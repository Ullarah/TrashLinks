import time

from flask import redirect, session, url_for
from markupsafe import escape

from app import init_session
from database import get_post, delete_post, add_vote_to_post, add_report_to_post, get_votes_on_post, \
    get_datetime_on_post, get_reports_on_post


def check_already_vote_or_old(post_id, username):
    seconds_since_post = int(time.time() - get_datetime_on_post(post_id))
    return True if username in get_votes_on_post(post_id) or seconds_since_post > 86400 else False


def check_already_report(post_id, username):
    return True if username in get_reports_on_post(post_id) else False


def route(action, post_id):
    init_session()
    if 'logged_in' in session:
        if session['logged_in'] and int(post_id) > 0:
            if action == 'delete':
                if get_post(post_id) is not None:
                    delete_post(post_id, escape(session['username']))
            if action == 'upvote':
                if not check_already_vote_or_old(post_id, escape(session['username'])):
                    add_vote_to_post(post_id, escape(session['username']))
            if action == 'report':
                if not check_already_report(post_id, escape(session['username'])):
                    add_report_to_post(post_id, escape(session['username']))
    return redirect(url_for('index'))
