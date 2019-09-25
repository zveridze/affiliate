import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', 'You will never guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQL_ALCHEMY_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.app'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
