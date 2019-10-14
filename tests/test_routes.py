import pytest
from app import db
from app.models import User


@pytest.fixture()
def db_test_data(app):
    with app.app_context():
        u = User(email='some@mail.ru')
        u.set_password('123')
        db.session.add(u)
        yield
        db.session.rollback()


def test_register(setup):
    rv = setup.post('/register', data=dict(email='test@mail.ru',
                                           password=123,
                                           password2=123), follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'Registration completed successfully' in rv.data


def test_register_user_already_exist(db_test_data, setup):
    rv = setup.post('/register', data=dict(email='some@mail.ru',
                                           password='123',
                                           password2='123'), follow_redirects=True)
    assert b'Sorry, email already exist.' in rv.data


def test_login_valid(setup):
    rv = setup.post('/login', data=dict(email='test@mail.ru',
                                        password=123), follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'Logout' in rv.data


def test_login_invalid(setup):
    rv = setup.post('/login', data=dict(email='invalid@mail.ru',
                                        password='123'), follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'User with provided credentials does not exist.' in rv.data


@pytest.mark.parametrize('url',
                         ['/dashboard', '/links', '/profile', '/change_password', '/report/all_actions_report',
                          '/report/all_links_report', '/report/all_days_report'])
def test_not_authenticated_user_open_links(setup, url):
    rv = setup.get(url, follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'Please log in to access this page.' in rv.data


def test_not_authenticated_user_open_profile(setup):
    rv = setup.post('/links', data=dict(name='test', site='https://vk.com'), follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'Please log in to access this page.' in rv.data

