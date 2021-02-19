import time

from flask import redirect, render_template, request, session, url_for
from markupsafe import escape, Markup

from app import alert_telegram_channel, list_of_tags, init_session
from database import insert_post, edit_post, get_post


def route(post_id):
    init_session()
    if post_id is None:
        if request.method == 'POST':
            user = escape(session['username'])
            title, url, tags = request.form['link-title'], request.form['link-url'], request.form['link-tags']
            insert_post(user, escape(title), escape(url), escape(tags))
            alert_telegram_channel(f'<b>[{tags}] {title}</b>\n<i>Posted by {user}</i>\n<a href="{url}">Link</a>')
            return redirect(url_for('index'))
        else:
            return render_template('submit.html', options=list_of_tags())
    else:
        if isinstance(int(post_id), int):
            if request.method == 'POST':
                title, url, tags = request.form['link-title'], request.form['link-url'], request.form['link-tags']
                edit_post(post_id, escape(title), escape(url), escape(tags))
                return redirect(url_for('index'))
            else:
                post = get_post(post_id)
                no_ownership = True if post.username != escape(session['username']) else False
                restricted_edit = True if (int(time.time()) - post.datetime) > 86400 else False
                return render_template('edit.html', options=list_of_tags(), id=post.id, title=Markup(post.title),
                                       url=post.url, tag=post.tags, no_ownership=no_ownership,
                                       restricted_edit=restricted_edit)
        else:
            return redirect(url_for('index'))
