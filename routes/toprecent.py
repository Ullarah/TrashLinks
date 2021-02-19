from flask import render_template

from app import init_session, post_reformat


def route(top_or_recent, template):
    init_session()
    posts = []

    for post in top_or_recent:
        posts.append(post_reformat(post))

    return render_template(f'{template}.html', posts=posts)
