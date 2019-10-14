from app.models import User, Link
from datetime import datetime


def test_password_hashing(setup):
    test_user = User(email='bla@mail.ru')
    test_user.set_password('cat')
    assert test_user.password_hash is not 'cat'


def test_password_valid_checking(setup):
    test_user = User(email='bla@mail.ru')
    test_user.set_password('cat')
    assert test_user.check_password('cat') is True


def test_password_invalid_checking(setup):
    test_user = User(email='bla@mail.ru')
    test_user.set_password('cat')
    assert test_user.check_password('dog') is False


def test_link_hashing(setup):
    test_link = Link(name='test', site='test.ru')
    test_link.generate_hash()
    assert test_link.hash_str is not datetime.utcnow()
