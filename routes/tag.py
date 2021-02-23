from flask import render_template, request, session

from core.function import post_reformat, init_session
from core.database import get_all_posts_with_tag


def route(tag):
    init_session()
    list_of_posts = []
    page = request.args.get('p', 1, type=int)
    page_info = get_all_posts_with_tag(tag, page)
    for post in page_info.items:
        list_of_posts.append(post_reformat(post))
    return render_template(f'{session["view_mode"]}/index.html', page=page_info, posts=list_of_posts)
