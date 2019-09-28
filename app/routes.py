from flask import render_template, redirect, url_for, flash, session
from flask_login import current_user, login_user, login_required, logout_user
from app.forms import LoginForm, RegistrationForm
from app import app, db
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user, session=session)


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
        return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    messenger_type=form.messenger_type.data,
                    messenger=form.messenger.data)

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration completed successfully')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
