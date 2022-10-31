import pytest
from game.routes.main import app

@pytest.fixture
def api():
    client = app.test_client()
    return client