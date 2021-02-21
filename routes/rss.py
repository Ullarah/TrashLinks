import datetime
import html

from flask import make_response
from feedgen.feed import FeedGenerator
from markupsafe import Markup


from core.function import init_session
from core.database import get_all_posts_for_rss, get_all_user_posts_for_rss


def route(user):
    init_session()
    fg = FeedGenerator()
    fg.title('Quisquiliae')
    fg.subtitle('Trash bag of links')
    fg.generator('Quisquiliae')
    fg.link(href='https://quisquiliae.com')
    fg.logo('http://quisquiliae.com/static/img/logo.png')
    fg.language('en')

    rss_posts = get_all_posts_for_rss() if user is None else get_all_user_posts_for_rss(user)

    for post in reversed(rss_posts):
        post_title = Markup((post.title[:60] + '...') if len(post.title) > 60 else post.title)
        fe = fg.add_entry()
        fe.title(f'[{post.tags}] {post_title}')
        fe.link(href=html.unescape(Markup(post.url)))
        fe.author(name=post.username)
        fe.pubDate(datetime.datetime.fromtimestamp(post.datetime).strftime('%c +10'))
        fe.updated(datetime.datetime.fromtimestamp(post.updated).strftime('%c +10'))

    response = make_response(fg.rss_str(pretty=True))
    response.headers.set('Content-Type', 'application/rss+xml')

    return response
