import pytest

from yumroad import create_app
from yumroad.models import db

@pytest.fixture
def app():
    return create_app('test')

@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()