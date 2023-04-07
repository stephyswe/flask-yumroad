import pytest
from flask import url_for
from flask_login import login_user

from yumroad import create_app
from yumroad.models import db, User
from yumroad.extensions import login_manager

@pytest.fixture
def app():
    app =  create_app('test')
    yield app

@pytest.fixture
def init_database():
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture
def authenticated_request(client):
    new_user = User.create("test@example.com", "examplepass")
    db.session.add(new_user)
    db.session.commit()

    response = client.post(url_for('user.login'), data={
        'email': "test@example.com",
        'password': "examplepass"
    }, follow_redirects=True)
    yield client