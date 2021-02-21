import time

from flask import redirect, render_template, request, session, url_for
from markupsafe import escape, Markup

from app import alert_telegram_channel, check_for_valid_title, check_for_valid_url,\
    check_for_valid_tags, list_of_tags, init_session
from database import insert_post, edit_post, get_post


def post_check(title, url, tags):
    if not check_for_valid_title(escape(title)):
        return False, 'title'
    if not check_for_valid_url(escape(url)):
        return False, 'url'
    if not check_for_valid_tags(escape(tags)):
        return False, 'tags'
    return True


def route(post_id):
    init_session()
    if post_id is None:
        if request.method == 'POST':
            user = escape(session['username'])
            title, url, tags = request.form['link-title'], request.form['link-url'], request.form['link-tags']
            is_post_valid = post_check(title, url, tags)
            if is_post_valid[0]:
                insert_post(user, escape(title), escape(url), escape(tags))
                alert_telegram_channel(f'<b>[{tags}] {title}</b>\n<i>Posted by {user}</i>\n<a href="{url}">Link</a>')
                return redirect(url_for('index'))
            else:
                return render_template('submit.html', options=list_of_tags(), error=is_post_valid[1],
                                       title=title, url=url, tags=tags)
        else:
            return render_template('submit.html', options=list_of_tags())
    else:
        if isinstance(int(post_id), int):
            if request.method == 'POST':
                title, url, tags = request.form['link-title'], request.form['link-url'], request.form['link-tags']
                is_post_valid = post_check(title, url, tags)
                if is_post_valid[0]:
                    edit_post(post_id, escape(title), escape(url), escape(tags))
                    return redirect(url_for('index'))
                else:
                    return render_template('submit.html', options=list_of_tags(), error=is_post_valid[1],
                                           title=title, url=url, tags=tags)
            else:
                post = get_post(post_id)
                no_ownership = True if post.username != escape(session['username']) else False
                restricted_edit = True if (int(time.time()) - post.datetime) > 86400 else False
                return render_template('edit.html', options=list_of_tags(), id=post.id, title=Markup(post.title),
                                       url=post.url, tag=post.tags, no_ownership=no_ownership,
                                       restricted_edit=restricted_edit)
        else:
            return redirect(url_for('index'))
