from app.models import User
from app.api.serializer import ActionObject, LinkObject
from app import create_app, redis_client
import json
import csv

app = create_app()
app.app_context().push()


def links_report_task(user_id):
    user = User.query.get(user_id)
    links = user.links
    link_obj = LinkObject()
    with open('links_reports.csv', 'w+') as file:
        csv_writer = csv.DictWriter(file, fieldnames=link_obj.dump(links[0]).keys())
        csv_writer.writeheader()
        for link in links:
            csv_writer.writerow(link_obj.dump(link))


def caching_report(user_id):
    try:
        bytes(user_id)
    except TypeError:
        return 'Invalid redis key type'

    user = User.query.get(user_id)
    action_obj = ActionObject()
    actions_list = []
    for link in user.links:
        for action in link.actions:
            actions_list.append(action_obj.dump(action))

    redis_client.set(user_id, json.dumps(actions_list))
