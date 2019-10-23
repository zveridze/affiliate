from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app.models import User, Link
from app import db
from app.api.serializer import UserObject, LinkObject


api = Blueprint('api', __name__)


class UserView(MethodView):

    def get(self, id):
        user = User.query.get_or_404(id)
        user_obj = UserObject()
        return user_obj.dump(user)

    def post(self):
        data = request.get_json()
        # if 'password' not in data or 'email' not in data:
        #     return 'Email and password must be defined!'
        # if 'email' in data and User.query.filter_by(email=data['email']).first():
        #     return 'Email already used!'
        user_obj = UserObject()
        user = user_obj.load(data)
        print(user.email)
        return jsonify({'1': 1})
        # user.from_dict(data=user_obj.load(data), new=True)
        # db.session.add(user)
        # db.session.commit()
        # return user_obj.dump(user)


api_view = UserView.as_view('api')
api.add_url_rule('/users', view_func=api_view, methods=['POST'])
api.add_url_rule('/users/<int:id>', view_func=api_view, methods=['GET'])


class LinkView(MethodView):

    @api.route('/users/<int:user_id>/links', methods=['GET'])
    def get(self, user_id):
        links = Link.query.filter_by(user_id=user_id).all()
        links_obj = LinkObject(many=True)
        return jsonify(links_obj.dump(links))
