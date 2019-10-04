from flask import render_template, redirect, url_for, flash, session, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from app.forms import LoginForm, RegistrationForm, LinkForm, PersonalDataEditForm
from app import app, db
from app.models import User, Link, Click, Action


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
            flash('User with provided credentials does not exist.')
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
            return redirect(url_for('index'))
        else:
            flash('Sorry, email already exist.')
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user, session=session)


@app.route('/profile', methods=['get', 'post'])
@login_required
def profile():
    form = PersonalDataEditForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.messenger_type = form.messenger_type.data
        current_user.messenger = form.messenger.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.messenger_type.data = current_user.messenger_type
        form.messenger.data = current_user.messenger
    return render_template('profile.html', form=form)


@app.route('/links', methods=['get', 'post'])
@login_required
def links():
    links_list = Link.query.filter_by(user_id=current_user.id).order_by(Link.timestamp.desc()).all()
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(name=form.name.data, user_id=current_user.id)
        link.generate_hash()
        db.session.add(link)
        db.session.commit()
        return redirect(url_for('links'))

    return render_template('links.html', form=form, links_list=links_list)


@app.route('/redirect_link/<hash>')
def redirect_link(hash):
    link = Link.query.filter_by(hash_str=hash).first()
    if link:
        ip = request.remote_addr
        agent = request.headers.get('User-Agent')
        new_click = Click(ip_address=ip, user_agent=agent)
        new_click.is_click_first()
        db.session.add(new_click)
        db.session.commit()
        action = Action(link_id=link.id, click_id=new_click.id)
        db.session.add(action)
        db.session.commit()

    return redirect('https://vk.com')


@app.route('/reports/all_clicks')
@login_required
def all_clicks():
    clicks = (
        Click.query
        .join(Action)
        .join(Link)
        .filter_by(user_id=current_user.id)
        .order_by(Action.timestamp.desc()).all()
    )
    return render_template('all_clicks.html', clicks=clicks)
