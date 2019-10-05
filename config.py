import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', 'You will never guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQL_ALCHEMY_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.app'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOST = os.environ.get('HOST', '192.168.1.92')
    PORT = os.environ.get('PORT', 5000)
    URL_FOR_REDIRECT_LINK = '{0}:{1}/redirect_link'.format(HOST, int(PORT))

    MESSENGERS = [('None', 'None'),
                  ('skype', 'Skype'),
                  ('tele', 'Telegram'),
                  ('whatsapp', 'WatsApp'),
                  ('viber', 'Viber')]
