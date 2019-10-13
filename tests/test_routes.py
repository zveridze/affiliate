from app import create_app, db
from config import Config
import pytest
import tempfile


print(tempfile.mkstemp())


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


@pytest.fixture()
def setup():
    app = create_app(TestingConfig)
    app.app_context()
    app_context = app.test_client()
    app_context.testing = True
    db.create_all(app=app)
    return app_context


def test_register(setup):
    rv = setup.post('/register', data=dict(email='test@mail.ru',
                                           password=123,
                                           password2=123), follow_redirects=True)
    print(rv.data)
    print(rv.status)


def test_login(setup):
    rv = setup.post('/login', data=dict(email='test@mail.ru',
                                        password=123), follow_redirects=True)
    print(rv.data)
    print(rv.status)
