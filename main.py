from flask import Flask, render_template
from functions import check_db_schema

DB_NAME = 'users.db'


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print('gg')
    print(check_db_schema(DB_NAME))
    app.run(debug=False)
