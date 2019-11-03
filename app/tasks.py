from time import sleep
from app.models import User
from app import create_app


app = create_app()
app.app_context().push()


def links_report_task(seconds):
    user = User.query.get(1)
    print(user.email)
    print('Starting task')
    for i in range(seconds):
        print(i)
        sleep(1)
    print('Task end')
