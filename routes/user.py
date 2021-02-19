import datetime

from flask import render_template, session
from markupsafe import escape
from treelib import Tree

from app import init_session, post_reformat
from database import get_all_user_details, get_user_post_points, get_user_post_count, get_all_user_invitee, \
    get_all_top_posts, get_all_recent_updated_posts


def route(viewuser):
    init_session()
    short_password = False
    if 'short_password' in session and session['short_password']:
        session.pop('short_password', None)
        short_password = True
    if viewuser is not None:
        user_request = escape(viewuser)
        details = get_all_user_details(user_request)
        if details is None:
            return render_template('user.html', viewuser=escape(viewuser), error=True)
        points, post_count = get_user_post_points(user_request), get_user_post_count(user_request)
        top_posts, recent_posts = [], []
        for post in get_all_top_posts(escape(viewuser)):
            top_posts.append(post_reformat(post))
        for post in get_all_recent_updated_posts(escape(viewuser)):
            recent_posts.append(post_reformat(post))
        can_see_invite_code = True if user_request == escape(session['username']) else False
        return render_template('user.html', viewuser=escape(viewuser), points=points, about_me=details.about_me,
                               last_login=datetime.datetime.fromtimestamp(details.last_login).strftime('%c'),
                               invited_by=details.invited_by, can_see_invite_code=can_see_invite_code,
                               invite_code=details.invite_code, submissions=post_count, short_password=short_password,
                               num_posts=len(top_posts), top_posts=top_posts, recent_posts=recent_posts)
    else:
        tree = Tree()
        tree.create_node('overseer', 'overseer')
        invitees = get_all_user_invitee()
        count = 1
        for u, i in invitees:
            if u != 'overseer':
                count += 1
                tree.create_node(u, parent=i)
        return render_template('user_tree.html', viewuser=escape(viewuser), tree=tree.show(stdout=False), total=count)
