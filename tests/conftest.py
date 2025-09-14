import pytest
import os

# Set Environment Variable
os.environ["ENABLE_PROXY_HEADERS"] = 'true'

from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
