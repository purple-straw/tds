import pytest
from app import create_app
from app.config.config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig())
    return app


@pytest.fixture
def client(app):
    return app.test_client()
