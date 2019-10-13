from app import create_app, db
from config import Config
import pytest


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)
    return app


@pytest.fixture()
def setup(request, app):
    app.app_context()
    app_context = app.test_client()
    app_context.testing = True
    return app_context


@pytest.fixture(scope='session', autouse=True)
def setup_db(request, app):
    with app.app_context():
        db.create_all()


def test_register(setup):
    rv = setup.post('/register', data=dict(email='test@mail.ru',
                                           password=123,
                                           password2=123), follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'Registration completed successfully' in rv.data


def test_login(setup):
    rv = setup.post('/login', data=dict(email='test@mail.ru',
                                        password=123), follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'Logout' in rv.data
