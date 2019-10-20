from flask import Blueprint, jsonify, request
from app.models import User
from app import db


api = Blueprint('api', __name__)


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


@api.route('/users', methods=['POST'])
def set_user():
    data = request.get_json()
    if 'password' not in data or 'email' not in data:
        return 'Email and password must be defined!'
    if 'email' in data and User.query.filter_by(email=data['email']).first():
        return 'Email already used!'
    user = User()
    user.from_dict(data=data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())

