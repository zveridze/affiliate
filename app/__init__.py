from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'index'
bootstrap = Bootstrap(app)


if __name__ == '__main__':
    app.run(debug=True)


from app import models, routes


@login.user_loader
def load_user(ID):
    return models.User.query.get(int(ID))
