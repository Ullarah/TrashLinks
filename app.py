import datetime
import os
import re
import time
from base64 import b64encode
from urllib.parse import urlparse

import requests
from better_profanity import profanity
from flask import Flask, redirect, render_template, session, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
from tldextract import tldextract
from waitress import serve

import database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(32)

db = SQLAlchemy(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico')


def init_session():
    for s in ['logged_in', 'username', 'current_page', 'dark_mode']:
        if s not in session:
            session['logged_in'] = False
            session['username'] = None
            session['current_page'] = 0
            session['dark_mode'] = False


def generate_code(length=8):
    return ''.join(c for c in b64encode(os.urandom(length)).decode('utf-8')[:-1] if c.isalnum())


def alert_telegram_channel(html_text):
    try:
        chat_id = '-1001174383932'
        bot_key = '1693414368:AAEYx_tdcUaPrzxivTPFX107wnXG0iqjvts'

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


@app.route('/up/<post_id>')
def upvote(post_id=0):
    from routes import post as run
    return run.route('upvote', post_id)


@app.route('/rp/<post_id>')
def report(post_id=0):
    from routes import post as run
    return run.route('report', post_id)


@app.route('/rm/<post_id>')
def remove(post_id=0):
    from routes import post as run
    return run.route('delete', post_id)


@app.route('/pw/', methods=['GET', 'POST'])
def change_password():
    from routes import password as run
    return run.route()


@app.route('/')
def index():
    from routes import index as run
    return run.route()


@app.route('/l/', methods=['GET', 'POST'])
def login():
    from routes import login as run
    return run.route()


@app.route('/o/')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/i/')
@app.route('/i/<code>', methods=['GET', 'POST'])
def invite(code=None):
    from routes import invite as run
    return run.route(code)


@app.route('/f/', methods=['GET', 'POST'])
def forgot():
    from routes import forgot as run
    return run.route()


@app.route('/m/', methods=['GET', 'POST'])
@app.route('/m/edit/<post_id>', methods=['GET', 'POST'])
def submit(post_id=None):
    from routes import submit as run
    return run.route(post_id)


@app.route('/g/')
@app.route('/g/<tag>')
def tags(tag=None):
    if not tag:
        return render_template('tags.html', tag_count=database.get_tag_count())
    else:
        from routes import tag as run
        return run.route(tag)


@app.route('/s/', methods=['GET'])
def search():
    from routes import search as run
    return run.route()


@app.route('/u/')
@app.route('/u/<viewuser>')
def user(viewuser=None):
    from routes import user as run
    return run.route(viewuser)


@app.route('/d/')
@app.route('/d/<domain_urls>')
def domains():
    return render_template('domains.html')


@app.route('/a/')
def about():
    return render_template('about.html')


@app.route('/r/')
def recent():
    from routes import toprecent as run
    return run.route(database.get_all_recent_updated_posts(), 'recent')


@app.route('/t/')
def top():
    from routes import toprecent as run
    return run.route(database.get_all_top_posts(), 'top')


@app.route('/b/')
@app.route('/b/<viewuser>')
def subscribe(viewuser=None):
    from routes import rss as run
    return run.route(viewuser)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=f'{error.code} {error.name}')


if __name__ == '__main__':
    profanity.load_censor_words()
    database.init()
    app.run(debug=True, host="127.0.0.1", port="3000")
    # app.run(debug=True, host="0.0.0.0", port="3000")
    # serve(app, host='0.0.0.0', port=3000, url_scheme='https', threads=10)
