from flask import redirect, url_for, flash, render_template, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm
from app.models import User, db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not user.check_password(form.password.data):
            flash('User with provided credentials does not exist.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        check_user = User.query.filter_by(email=form.email.data).first()
        if not check_user:
            user = User(email=form.email.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        messenger_type=form.messenger_type.data,
                        messenger=form.messenger.data)

            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration completed successfully')
            return redirect(url_for('auth.login'))
        else:
            flash('Sorry, email already exist.')
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/change_password', methods=['get', 'post'])
@login_required
def change_password():
    user = User.query.get(current_user.id)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/profile')
    return render_template('auth/change_password.html', form=form)
