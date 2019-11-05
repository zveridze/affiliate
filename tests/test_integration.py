from app import db
from app.models import User
import pytest
from flask_jwt_extended import create_access_token
from app.api.serializer import UserObject
import json


@pytest.fixture()
def test_user_create(app):
    with app.app_context():
        user = User(email='text@mail.ru', is_admin=True)
        user.set_password('123')
        db.session.add(user)
        yield user
        db.session.rollback()


def test_users_list_get(test_user_create, setup):
    user_obj = UserObject()
    access_token = create_access_token(identity=user_obj.dump(test_user_create))
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token)
    }
    resp = setup.get(path='/api/users', content_type='application/json', headers=headers)
    assert len(resp.json) == 1
    assert resp.status_code is 200


def test_user_get(test_user_create, setup):
    user_obj = UserObject()
    test_user_create.id = 1
    access_token = create_access_token(identity=user_obj.dump(test_user_create))
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token)
    }
    resp = setup.get(path='/api/users/1', content_type='application/json', headers=headers)
    assert resp.json['id'] == 1
    assert resp.status_code is 200


def test_user_post(setup):
    data = {
        'email': 'test_api@mail.ru',
        'password_hash': '123',
        'first_name': 'Some',
        'last_name': 'Test'
    }
    user = setup.post(path='/api/register', content_type='application/json', data=json.dumps(data))
    access_token = create_access_token(identity=user.json)
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token)
    }
    resp = setup.get(path='/api/users/1', content_type='application/json', headers=headers)
    assert resp.json['email'] == data['email']
    assert resp.json['id'] == 1


def test_user_post_miss_password(setup):
    data = {
        'email': 'test@mail.ru',
        'first_name': 'Some',
        'last_name': 'Test'
    }
    resp = setup.post(path='/api/register', content_type='application/json', data=json.dumps(data))
    assert resp.json == '\'password_hash\' is a required property'
    assert resp.status_code == 400


def test_user_post_miss_email(setup):
    data = {
        'password_hash': 123,
        'first_name': 'Some',
        'last_name': 'Test'
    }
    resp = setup.post(path='/api/register', content_type='application/json', data=json.dumps(data))
    assert resp.json == '\'email\' is a required property'
    assert resp.status_code == 400
