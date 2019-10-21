from flask_marshmallow import Marshmallow

ma = Marshmallow()


class UserObject(ma.Schema):

    class Meta:
        additional = ('id', 'email', 'first_name', 'last_name', 'messenger_type', 'messenger', 'password')
        load_only = ('password', )


class LinkObject(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'site', 'hash_str', 'date_create', 'user_id')
