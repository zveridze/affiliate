from app import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    messenger_type = db.Column(db.String, index=True)
    messenger = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    programs = db.relationship('Program', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(ID):
    return User.query.get(int(ID))


class Program(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


