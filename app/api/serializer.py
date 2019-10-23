from flask_marshmallow import Marshmallow
from marshmallow import post_load
from app.models import User

ma = Marshmallow()


class UserObject(ma.Schema):

    class Meta:
        additional = ('id', 'email', 'first_name', 'last_name', 'messenger_type', 'messenger', 'password_hash')
        load_only = ('password_hash', )

    @post_load
    def make_user(self, data, **kwargs):
        user = User(**data)
        if 'password_hash' in data:
            user.set_password(data['password_hash'])

        return user


class LinkObject(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'site', 'hash_str', 'date_create', 'user_id')
