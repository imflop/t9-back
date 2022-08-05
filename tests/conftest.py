import pytest

from t9_back.lib.settings import AppSettings
from t9_back.lib.setup_app import setup_app


@pytest.fixture()
def settings():
    return AppSettings()


@pytest.fixture()
def app(settings):
    return setup_app(settings)
