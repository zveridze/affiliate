from flask import Flask
from config import Config
from app.models import db
from app import models
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from app.auth.routes import auth
from app.main.routes import main
from app.report.routes import report


migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(report)

    return app


@login.user_loader
def load_user(ID):
    return models.User.query.get(int(ID))
