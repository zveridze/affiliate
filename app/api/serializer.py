from flask_marshmallow import Marshmallow

ma = Marshmallow()


class UserObject(ma.Schema):

    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name', 'messenger_type', 'messenger', 'password_hash')
        dump_only = ('password_hash', 'email')


class LinkObject(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'site', 'hash_str', 'date_create', 'user_id')
