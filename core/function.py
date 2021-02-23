import datetime
import os
import re
import time
from base64 import b64encode
from json import loads
from urllib.parse import urlparse

import requests
from flask import session
from markupsafe import Markup
from tldextract import tldextract


def get_config_value(value):
    return loads(open('data/config.json', 'r').read())[value]


def init_session():
    for s in ['logged_in', 'username', 'current_page', 'dark_mode', 'view_mode']:
        if s not in session:
            session['logged_in'] = False
            session['username'] = None
            session['current_page'] = 0
            session['dark_mode'] = False
            session['view_mode'] = 'desktop'


def generate_code(length=8):
    return ''.join(c for c in b64encode(os.urandom(length)).decode('utf-8')[:-1] if c.isalnum())


def alert_telegram_channel(html_text):
    try:
        telegram_config = get_config_value('telegram')
        chat_id = telegram_config['chat_id']
        bot_key = telegram_config['bot_key']

        url = f'https://api.telegram.org/bot{bot_key}/sendMessage'
        data = {'chat_id': chat_id, 'parse_mode': 'HTML', 'text': html_text}

        requests.post(url=url, data=data)
    except requests.exceptions as e:
        print(f'Post submitted, no notification done.\n{e}')


def human_datetime(post_time):
    time_since_post = 'unknown'
    time_type = {
        'minute': 60,
        'hour': 60 * 60,
        'day': 24 * 60 * 60,
        'week': 7 * 24 * 60 * 60,
        'month': 30 * 7 * 24 * 60 * 60,
        'year': 364 * 30 * 7 * 24 * 60 * 60
    }

    seconds = int(time.time()) - post_time

    if seconds < 60:
        s = '' if seconds == 1 else 's'
        time_since_post = f'{seconds} second{s} ago'

    for k, v in time_type.items():
        if seconds > v:
            v = divmod(seconds, v)[0]
            s = '' if v == 1 else 's'
            time_since_post = f'{v} {k}{s} ago'

    return time_since_post


def list_of_tags():
    return [
        'naughty', 'eyecandy', 'gaming', 'hardware', 'news', 'sad', 'happy', 'instahoe', 'image', 'video', 'listen',
        'wtf', 'art', 'retro', 'geek', 'cool', 'play', 'funny', 'classic', 'lame', 'gross', 'sport', 'meme', 'serious'
    ]


def check_for_valid_tags(post_tags):
    result = post_tags.replace(" ", "") in list_of_tags()
    return True if result and len(post_tags) <= 8 else False


def check_for_valid_url(post_url):
    result = all([urlparse(post_url).scheme in ["http", "https"], urlparse(post_url).netloc, urlparse(post_url).path])
    return True if result and len(post_url) >= 12 else False


def check_for_valid_title(post_title):
    result = re.fullmatch(re.compile(r"[A-Za-z0-9+=\-_()#!?,.\s]+"), post_title)
    return True if result and len(post_title) >= 16 else False


def post_reformat(post):
    return [
        post.id,                                                                      # 0  post id
        Markup((post.title[:120] + '...') if len(post.title) > 120 else post.title),  # 1  post title
        Markup(post.url),                                                             # 2  full url
        tldextract.extract(post.url).registered_domain,                               # 3  domain only url
        Markup(post.username),                                                        # 4  user name
        datetime.datetime.fromtimestamp(post.datetime).strftime('%c'),                # 5  tooltip time
        human_datetime(post.datetime),                                                # 6  time since post
        post.tags,                                                                    # 7  tags
        len(post.votes.split(';')),                                                   # 8  votes
        len(post.reports.split(';')),                                                 # 9  reports
        int(time.time() - post.datetime)                                              # 10 epoch seconds
    ]
