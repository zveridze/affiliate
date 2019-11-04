from app.models import Action, Link, db
from flask import render_template, redirect, url_for, Blueprint, request
from flask_login import login_required, current_user
from sqlalchemy import func, distinct


report = Blueprint('report', __name__)


@report.route('/report/all_actions_report')
@login_required
def all_actions_report():
    page = request.args.get('page', 1, type=int)
    actions = (
        Action.query
        .join(Link)
        .filter_by(user_id=current_user.id)
        .order_by(Action.timestamp.desc()).paginate(page=page, per_page=25)
    )
    prev_page = url_for('report.all_actions_report', page=actions.prev_num) if actions.has_prev else None
    next_page = url_for('report.all_actions_report', page=actions.next_num) if actions.has_next else None
    return render_template('reports/all_actions_report.html',
                           actions=actions.items,
                           prev=prev_page,
                           next=next_page,
                           )


@report.route('/report/all_links_report')
@login_required
def all_links_report():
    page = request.args.get('page', 1, type=int)
    actions = (
        Action.query.
        join(Link).
        filter_by(user_id=current_user.id).
        with_entities(Link,
                      func.count(Action.ip_address).label('clicks'),
                      func.count(distinct(Action.ip_address)).label('unique'),
                      func.count(Action.purchase_amount).label('purchases'),
                      func.sum(Action.purchase_amount).label('amount')).
        group_by(Action.link_id).paginate(page=page, per_page=25)
    )
    prev_page = url_for('report.all_links_report', page=actions.prev_num) if actions.has_prev else None
    next_page = url_for('report.all_links_report', page=actions.next_num) if actions.has_next else None
    return render_template('reports/all_links_report.html',
                           actions=actions.items,
                           prev=prev_page,
                           next=next_page,
                           )


@report.route('/report/current_link_report/<link_id>')
@login_required
def current_link_report(link_id):
    page = request.args.get('page', 1, type=int)
    link = Link.query.filter_by(id=link_id, user_id=current_user.id).first()
    if not link:
        return redirect(url_for('main.index'))
    dates = (
        Action.query.
        join(Link).
        filter_by(id=link_id).
        with_entities(func.strftime('%Y-%m-%d', Action.timestamp).label('date'),
                      func.count(Action.ip_address).label('actions'),
                      func.count(distinct(Action.ip_address)).label('unique'),
                      func.sum(Action.purchase_amount).label('purchases'),
                      func.count(Action.purchase_amount).label('amount')).
        group_by(func.strftime('%Y-%m-%d',  Action.timestamp)).paginate(page=page, per_page=25))
    prev_page = url_for('report.current_link_report', page=dates.prev_num) if dates.has_prev else None
    next_page = url_for('report.current_link_report', page=dates.next_num) if dates.has_next else None
    return render_template('main/current_link_report.html',
                           dates=dates.items,
                           link=link,
                           prev=prev_page,
                           next=next_page,
                           )


@report.route('/report/all_days_report')
@login_required
def all_days_report():
    links = Link.query.filter_by(user_id=current_user.id).all()
    links_id = [link.id for link in links]

    action = (
        Action.query.
        filter(Action.link_id.in_(links_id)).
        with_entities(Action.ip_address.label('ip_address'),
                      Action.link_id.label('link_id'),
                      func.strftime('%Y-%m-%d', Action.timestamp).label('date')).
        group_by(Action.link_id, Action.ip_address).subquery())

    action_count = (
        db.session.query(func.count(action.c.ip_address).label('first'),
                         action.c.date.label('date')).
        group_by(action.c.date).subquery())

    dates = (
        db.session.query(func.strftime('%Y-%m-%d', Action.timestamp).label('date'),
                         action_count.c.first.label('first'),
                         func.count(Action.ip_address).label('ip'),
                         func.sum(Action.purchase_amount).label('purchases'),
                         func.count(Action.purchase_amount).label('amount'),
                         ).filter(Action.link_id.in_(links_id)).
        outerjoin(action_count, (action_count.c.date == func.strftime('%Y-%m-%d', Action.timestamp))).
        group_by(func.strftime('%Y-%m-%d', Action.timestamp)).all())
    return render_template('reports/all_days_report.html', dates=dates)
