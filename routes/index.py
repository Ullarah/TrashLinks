from flask import render_template, request, session

from core.function import post_reformat, init_session
from core.database import get_all_posts


def route():
    init_session()
    list_of_posts = []
    page = request.args.get('p', 1, type=int)
    if session["view_mode"] == 'desktop':
        page_info = get_all_posts(page)
    else:
        page_info = get_all_posts(page, 5)
    for post in page_info.items:
        list_of_posts.append(post_reformat(post))
    return render_template(f'{session["view_mode"]}/index.html', page=page_info, posts=list_of_posts)
