from flask import Flask, render_template, request
from functions import do_sql

DB_NAME = 'users.db'
SQL_WHAT_TABLES = "SELECT name FROM sqlite_master WHERE type='table';"
SQL_CREATE_TABLES = "CREATE TABLE users(id INTEGER PRIMARY KEY, email, password);"

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/check_login_pass', methods=['GET', 'POST'])
def check_login_pass():
    if request.method == 'POST':
        print(request.form)
        return 'under construction'
    if request.method == 'GET':
        return 'it is a GET!'


@app.route('/write_to_database', methods=['GET', 'POST'])
def write_to_database():
    if request.method == 'POST':
        return 'POST write_to_database'
    if request.method == 'GET':
        return 'it is a GET!'


if __name__ == '__main__':
    # TODO проверять не только существование, но и структуру
    if not do_sql(DB_NAME, SQL_WHAT_TABLES):
        do_sql(DB_NAME, SQL_CREATE_TABLES)
    app.run(debug=False)
