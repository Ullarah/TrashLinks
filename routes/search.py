from flask import render_template, request

from core.function import post_reformat, init_session
from core.database import search_for_posts


def route():
    init_session()
    if request.method == 'GET':
        if 'q' in request.args:
            query = request.args.get('q', 1, type=str)
            if not query.strip() or query.isspace():
                return render_template('search.html', empty_query=True)
        else:
            return render_template('search.html')
        term = 'title'
        if query.startswith('!tag'):
            term = 'tag'
            query = query.replace('!tag ', '', 1)
        if query.startswith('!domain'):
            term = 'domain'
            query = query.replace('!domain ', '')
        if query.startswith('!user'):
            term = 'user'
            query = query.replace('!user ', '')
        list_of_posts = []
        page = request.args.get('p', 1, type=int)
        page_total, page_info = search_for_posts(page, query, term)
        if len(page_info.items) > 0:
            for post in page_info.items:
                list_of_posts.append(post_reformat(post))
            return render_template('search.html', is_valid_search=True, query=query, search_count=page_total,
                                   page=page_info, posts=list_of_posts)
        else:
            return render_template('search.html', nothing_found=True)
    else:
        return render_template('search.html')
