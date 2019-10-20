from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import hashlib
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    messenger_type = db.Column(db.String, index=True)
    messenger = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    links = db.relationship('Link', backref='user')

    def to_dict(self):
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'messenger_type': self.messenger_type,
            'messenger': self.messenger
        }

        return data

    def from_dict(self, data, new=False):
        for item in data.items():
            setattr(self, item[0], item[1])
        if new and 'password' in data:
            self.set_password(data['password'])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
    type_id = db.Column(db.Integer, nullable=False)
    ip_address = db.Column(db.String(40), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    purchase_amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
