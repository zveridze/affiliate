from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import hashlib
from flask_sqlalchemy import SQLAlchemy
from flask import current_app


db = SQLAlchemy()


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)  # noqa
    email = db.Column(db.String(128), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    messenger_type = db.Column(db.String, index=True)
    messenger = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    links = db.relationship('Link', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_report(self):
        current_app.task_queue.enqueue('app.tasks.links_report_task', self.id)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # noqa
    name = db.Column(db.String(60))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    site = db.Column(db.String(120), index=True, nullable=False)
    hash_str = db.Column(db.String(20), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    actions = db.relationship('Action', backref='link')

    def generate_hash(self):
        hash_date = str(datetime.utcnow()).encode('utf-8')
        self.hash_str = hashlib.sha256(hash_date).hexdigest()


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # noqa
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
    type_id = db.Column(db.Integer, nullable=False)
    ip_address = db.Column(db.String(40))
    user_agent = db.Column(db.String)
    purchase_amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Action, self).__init__(**kwargs)
