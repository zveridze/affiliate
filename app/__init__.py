from flask import Flask
from config import Config
from app.models import db
from app import models, db
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_redis import FlaskRedis
from app.auth.routes import auth
from app.main.routes import main
from app.report.routes import report
from app.api.serializer import ma
from app.api.endpoints import api_bp
from flask_jwt_extended import JWTManager
from redis import Redis
import rq
from rq_scheduler import Scheduler

migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
jwt = JWTManager()
redis_client = FlaskRedis()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    redis_client.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    jwt.init_app(app)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('affiliate', connection=app.redis)
    app.scheduler = Scheduler(queue=app.task_queue, connection=app.redis)

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(report)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


@login.user_loader
def load_user(ID):
    return models.User.query.get(int(ID))
