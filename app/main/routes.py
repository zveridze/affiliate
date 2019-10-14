from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_required
from flask.views import MethodView
from app.main.forms import LinkForm, PersonalDataEditForm
from app.models import Link, Action, db
from datetime import datetime
from sqlalchemy import func, distinct


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    data = (
        Action.query.
        join(Link).
        filter_by(user_id=user.id).
        with_entities(func.count(Action.ip_address).label('ip'),
                      func.count(distinct(Action.ip_address)).label('unique'),
                      func.count(Action.purchase_amount).label('purchases'),
                      func.sum(Action.purchase_amount).label('amount')).first())
    return render_template('main/dashboard.html', user=user, data=data)


class ProfileView(MethodView):

    @login_required
    def get(self):
        form = PersonalDataEditForm()
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.messenger_type.data = current_user.messenger_type
        form.messenger.data = current_user.messenger
        links = Link.query.filter_by(user_id=current_user.id).all()
        return render_template('main/profile.html', form=form, links=links)

    @login_required
    def post(self):
        form = PersonalDataEditForm()
        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.messenger_type = form.messenger_type.data
            current_user.messenger = form.messenger.data
            db.session.commit()
            flash('Your changes have been saved')
            return redirect(url_for('main.profile'))


@main.route('/links', methods=['get', 'post'])
@login_required
def links():
    links_list = Link.query.filter_by(user_id=current_user.id).order_by(Link.timestamp.desc()).all()
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(name=form.name.data, site=form.site.data, user_id=current_user.id)
        link.generate_hash()
        db.session.add(link)
        db.session.commit()
        return redirect(url_for('main.links'))

    return render_template('main/links.html', form=form, links_list=links_list)


@main.route('/redirect_link/<hash>')
def redirect_link(hash):
    link = Link.query.filter_by(hash_str=hash).first()
    if link:
        ip = request.remote_addr
        agent = request.headers.get('User-Agent')
        new_action = Action(link_id=link.id, type_id=1, ip_address=ip, user_agent=agent, timestamp=datetime.utcnow())
        db.session.add(new_action)
        db.session.commit()

    return redirect(link.site)


main.add_url_rule('/profile', view_func=ProfileView.as_view('profile'))