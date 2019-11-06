from flask_redis import FlaskRedis
from app.api.serializer import ActionObject
import json


redis_client = FlaskRedis()


def caching_report(user_id, actions):
    try:
        bytes(user_id)
    except TypeError:
        return 'Invalid redis key type'
    action_obj = ActionObject()
    dict_actions = [action_obj.dump(action) for action in actions]
    redis_client.append(user_id, json.dumps(dict_actions))
    return redis_client.get('1')
