import pytest
from config import Config
from app import create_app, db
from app.models import User, Link
from datetime import datetime


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class TestModels:

    def setup(self):
        print('1')
        self.app = create_app(Config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        print('2')
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        test_user = User(email='test@mail.ru')
        test_user.set_password('cat')
        assert test_user.password_hash is not 'cat'

    def test_password_valid_checking(self):
        test_user = User(email='test@mail.ru')
        test_user.set_password('cat')
        assert test_user.check_password('cat') is True

    def test_password_invalid_checking(self):
        test_user = User(email='test@mail.ru')
        test_user.set_password('cat')
        assert test_user.check_password('dog') is False

    def test_link_hashing(self):
        test_link = Link(name='test', site='test.ru')
        test_link.generate_hash()
        assert test_link.hash_str is not datetime.utcnow()
