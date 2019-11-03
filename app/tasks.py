from app.models import User
from app.api.serializer import LinkObject
from app import create_app
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
