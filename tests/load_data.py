import sqlite3
from datetime import datetime
import os

PATH_TO_DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.app')


def link_obj(iter):
    inserted_data = [
        {
            'name': 'test_name{0}'.format(iter),
            'site': 'https://google.com',
            'hash_str': str(iter),
            'timestamp': datetime.utcnow(),
            'user_id': 3
        }
    ]

    return inserted_data


def action_obj(item):
    inserted_data = [
        {
            'link_id': 1,
            'type_id': 1,
            'ip_address': '192.168.0.1:{0}'.format(item),
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:69.0) Gecko/20100101 Firefox/69.0',
            'purchase_amount': '1',
            'timestamp': datetime.utcnow(),
        }
    ]

    return inserted_data


def links_generator(item):
    conn = sqlite3.connect(PATH_TO_DB)

    for i in range(10001, item):
        link = link_obj(i)
        conn.execute(
            '''
            INSERT INTO Link (name, site, hash_str, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?);
            ''', (link[0]['name'], link[0]['site'], link[0]['hash_str'], link[0]['timestamp'], link[0]['user_id'])
        )

    conn.commit()
    conn.close()


def actions_generator(item):
    conn = sqlite3.connect(PATH_TO_DB)

    for i in range(item):
        action = action_obj(i)
        conn.execute(
            '''
            INSERT INTO Action (link_id, type_id, ip_address, user_agent, purchase_amount, timestamp)
            VALUES (?, ?, ?, ?, ?, ?);
            ''', (action[0]['link_id'], action[0]['type_id'], action[0]['ip_address'],
                  action[0]['user_agent'], action[0]['purchase_amount'], action[0]['timestamp'])
        )

    conn.commit()
    conn.close()


links_generator(20000)