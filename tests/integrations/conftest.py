import contextlib
import time
import uuid
from pathlib import Path

import psycopg2
import pytest
from docker import DockerClient
from docker.errors import ImageNotFound
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from alembic.command import upgrade
from alembic.config import Config

from ..factory_boys import Session


ROOT_DIR = Path(__file__).parent.parent.parent
POSTGRES_IMAGE = "postgres:11.6-alpine"
POSTGRES_CONTAINER_BASE_NAME = "postgres-test"


@pytest.fixture()
def client(app, settings):
    with TestClient(app=app, base_url="http://app") as client:
        yield client


@pytest.fixture(scope="session")
def pg_container():
    """Start the PostgreSQL container"""
    docker_client = DockerClient.from_env()
    ports = {"5432/tcp": None}
    host = "127.0.0.1"
    db_name = "test_database"
    username = "test_user"
    password = "password"
    generate_container_name = lambda x: f"{x}-{uuid.uuid4().hex}"

    try:
        docker_client.images.get(POSTGRES_IMAGE)
    except ImageNotFound:
        docker_client.images.pull(POSTGRES_IMAGE)

    container = docker_client.containers.create(
        image=POSTGRES_IMAGE,
        name=generate_container_name(POSTGRES_CONTAINER_BASE_NAME),
        detach=True,
        environment={
            "POSTGRES_DB": db_name,
            "POSTGRES_USER": username,
            "POSTGRES_PASSWORD": password,
        },
        ports=ports,
    )

    container.start()

    # Wait until ports are available
    while True:
        container.reload()
        container_ports = {k: v for k, v in container.ports.items() if v}
        if set(ports).issubset(container_ports):
            break
        time.sleep(0.05)

    # Wait until the container is ready
    while True:
        log = container.logs(tail=1)
        if "database system is ready to accept connections" in log.decode():
            break
        time.sleep(0.5)

    container_host_port = int(container.ports["5432/tcp"][0]["HostPort"])

    yield {
        "host": host,
        "port": container_host_port,
        "user": username,
        "password": password,
        "db": db_name,
        "dsn": f"postgresql://{username}:{password}@{host}:{container_host_port}/postgres",
    }

    container.kill(signal=9)
    container.remove(v=True, force=True)


@pytest.fixture(scope="session")
def pg_conf(pg_container):
    """Manage PostgreSQL settings"""
    return {
        "host": pg_container["host"],
        "port": pg_container["port"],
        "db": pg_container["db"],
        "user": pg_container["user"],
        "password": pg_container["password"],
        "dsn": f"{pg_container['dsn']}",
        "async_dsn": f"postgresql+asyncpg://{pg_container['user']}:{pg_container['password']}@{pg_container['host']}:{pg_container['port']}/{pg_container['db']}",
    }


@pytest.fixture(scope="session")
def system_db(pg_conf):
    conn = psycopg2.connect(dsn=pg_conf["dsn"])
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    yield cur
    cur.close()
    conn.close()


@pytest.fixture(scope="session")
def template_db(system_db):
    name = "templatedb"
    with contextlib.suppress(Exception):
        system_db.execute(f"DROP DATABASE {name}")
    system_db.execute(f"CREATE DATABASE {name}")
    return name


@pytest.fixture(scope="session")
def alembic_config(pg_conf, template_db):
    config = Config(f"{ROOT_DIR}/alembic.ini")
    config.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{pg_conf['user']}:{pg_conf['password']}@{pg_conf['host']}:{pg_conf['port']}/{template_db}",
    )
    return config


@pytest.fixture(scope="session")
def alembic_upgrade(alembic_config, system_db, pg_conf):
    with contextlib.suppress(Exception):
        system_db.execute(f"CREATE USER {pg_conf['user']} WITH SUPERUSER PASSWORD '{pg_conf['password']}'")
    upgrade(alembic_config, "head")


@pytest.fixture()
def create_db(system_db, pg_conf, alembic_upgrade, template_db):
    system_db.execute(f"DROP DATABASE IF EXISTS {pg_conf['db']}")
    system_db.execute(f"CREATE DATABASE {pg_conf['db']} WITH TEMPLATE {template_db}")


@pytest.fixture()
def engine(pg_conf):
    return create_async_engine(pg_conf["async_dsn"])


@pytest.fixture()
async def db(engine, create_db, pg_conf):
    _engine = create_engine(
        f"postgresql://{pg_conf['user']}:{pg_conf['password']}@{pg_conf['host']}:{pg_conf['port']}/{pg_conf['db']}",
        poolclass=NullPool,
    )
    Session.configure(bind=_engine)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    Session.close()
    Session.configure(engine=None)
