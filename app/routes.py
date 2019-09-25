from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user
from app.forms import LoginForm, RegistrationForm
from app import app, db
from app.models import User
from functions import do_sql

DB_NAME = 'users.db'
SQL_WHAT_TABLES = "SELECT name FROM sqlite_master WHERE type='table';"
SQL_CREATE_TABLES = "CREATE TABLE users" \
                    " (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL," \
                    " email TEXT UNIQUE NOT NULL," \
                    " password TEXT NOT NULL);"
SQL_CREATE_TESTER = "INSERT INTO users (email, password) VALUES ( 'tester', 'testerpass' );"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not user.check_password(form.password.data):
            flash('Most likely you have entered incorrect e-mail or password.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    phone=form.phone.data, messenger_type=form.messenger_type.data, messenger=form.messenger.data)

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration completed successfully')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/check_login_pass', methods=['GET', 'POST'])
def check_login_pass():
    if request.method == 'POST':
        print(dict(request.form))
        return render_template('cabinet.html')
    else:
        return 'method must be POST!'


@app.route('/write_to_database', methods=['GET', 'POST'])
def write_to_database():
    if request.method == 'POST':
        pair_key_value_from_request = dict(request.form)
        email = pair_key_value_from_request['email']
        password = pair_key_value_from_request['password']
        new_query = "SELECT email FROM users where email = {0}".format(email)
        print(do_sql(DB_NAME, new_query))
        return render_template('cabinet.html', email=email, password=password)
    else:
        return 'method must be POST!'


if __name__ == '__main__':
    # TODO проверять не только существование, но и структуру
    if not do_sql(DB_NAME, SQL_WHAT_TABLES):
        do_sql(DB_NAME, SQL_CREATE_TABLES)
        do_sql(DB_NAME, SQL_CREATE_TESTER)

    app.run(debug=False)
