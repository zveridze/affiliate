from app import db
from app.models import User
import pytest
import json


@pytest.fixture()
def db_context_data(app):
    with app.app_context():
        user = User(email='text@mail.ru')
        user.set_password('123')
        db.session.add(user)
        yield
        db.session.rollback()


def test_users_list_get(db_context_data, setup):
    resp = setup.get(path='/api/users', content_type='application/json')
    assert len(resp.json) == 1
    assert resp.status_code is 200


def test_user_get(db_context_data, setup):
    resp = setup.get(path='/api/users/1', content_type='application/json')
    assert resp.json['id'] == 1
    assert resp.status_code is 200


def test_user_post(setup):
    data = {
        'email': 'test_api@mail.ru',
        'password_hash': '123',
        'first_name': 'Some',
        'last_name': 'Test'
    }
    setup.post(path='/api/users', content_type='application/json', data=json.dumps(data))
    resp = setup.get(path='/api/users/1', content_type='application/json')
    assert resp.json['email'] == data['email']
    assert resp.json['id'] == 1


def test_user_post_miss_password(setup):
    data = {
        'email': 'test@mail.ru',
        'first_name': 'Some',
        'last_name': 'Test'
    }
    resp = setup.post(path='/api/users', content_type='application/json', data=json.dumps(data))
    assert resp.json == '\'password_hash\' is a required property'
    assert resp.status_code == 400


def test_user_post_miss_email(setup):
    data = {
        'password_hash': 123,
        'first_name': 'Some',
        'last_name': 'Test'
    }
    resp = setup.post(path='/api/users', content_type='application/json', data=json.dumps(data))
    assert resp.json == '\'email\' is a required property'
    assert resp.status_code == 400