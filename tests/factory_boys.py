from random import randint

import factory
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import orm

from t9_back.lib.dal.models.links import LinkModel


Session = orm.scoped_session(orm.sessionmaker())


def generate_id(obj, create, value):
    if hasattr(obj, "id") and obj.id is None:
        obj.id = value or randint(1, 1000000)


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"
        strategy = factory.BUILD_STRATEGY

    id = factory.PostGeneration(generate_id)


class LinkFactory(BaseFactory):
    class Meta:
        model = LinkModel

    original_url = factory.Faker("url")
    short_url = factory.Faker("url")
