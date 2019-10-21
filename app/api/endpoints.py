from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app.models import User, Link
from app import db
from app.api.serializer import UserObject, LinkObject


api = Blueprint('api', __name__)


class UserView(MethodView):

    def get(self, id):
        user = User.query.get_or_404(id)
        user_dict = UserObject()
        return user_dict.dump(user)

    def post(self):
        user_dict = UserObject()
        data = request.get_json()
        info = user_dict.load(data)
        print(info)
        return jsonify({'1': '1'})
        # if 'password' not in data or 'email' not in data:
        #     return 'Email and password must be defined!'
        # if 'email' in data and User.query.filter_by(email=data['email']).first():
        #     return 'Email already used!'
        # user = User()
        # user.from_dict(data=data)
        # db.session.add(user)
        # db.session.commit()
        # return jsonify(user.to_dict())


api_view = UserView.as_view('api')
api.add_url_rule('/users', view_func=api_view, methods=['POST'])
api.add_url_rule('/users/<int:id>', view_func=api_view, methods=['GET'])


class LinkView(MethodView):

    @api.route('/users/<int:id>/links', methods=['GET'])
    def get(self, id):
        links = Link.query.filter_by(user_id=id).all()
        links_obj = LinkObject(many=True)
        return jsonify(links_obj.dump(links))


# @api.route('/users/<int:id>', methods=['GET'])
# def get_user(id):
#     user = User.query.get_or_404(id)
#     user_dict = UserObject()
#     return user_dict.dump(user)
#
#
# @api.route('/users', methods=['POST'])
# def set_user():
#     data = request.get_json()
#     if 'password' not in data or 'email' not in data:
#         return 'Email and password must be defined!'
#     if 'email' in data and User.query.filter_by(email=data['email']).first():
#         return 'Email already used!'
#     user = User()
#     user.from_dict(data=data)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify(user.to_dict())
#
#
# @api.route('/users/<int:id>/links', methods=['GET'])
# def get_links(id):
#     links = Link.query.filter_by(user_id=id).all()
#     links_obj = LinkObject(many=True)
#     return jsonify(links_obj.dump(links))
