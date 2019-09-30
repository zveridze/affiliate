from app import db, app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import hashlib


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    messenger_type = db.Column(db.String, index=True)
    messenger = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    programs = db.relationship('Program', backref='user')
    links = db.relationship('Link', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(120), default=app.config['URL_FOR_LINK'])
    hash_str = db.Column(db.String(20), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def generate_hash(self):
        hash_date = str(self.timestamp).encode('utf-8')
        self.hash_str = hashlib.sha256(hash_date).hexdigest()[:20]
