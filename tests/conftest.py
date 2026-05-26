import pytest
from app import create_app
from extensions import db as _db


@pytest.fixture(scope="session")
def app():
    return create_app("testing")


@pytest.fixture
def client(app):
    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.session.remove()
        _db.drop_all()
