import os
import time

from sqlalchemy import desc

from core.function import get_config_value
from main import db


def insert_user(username, password, private_key, invited_by, invite_code):
    if not does_user_exist(username):
        db.session.add(User(
            username=username,
            password=password,
            private_key=private_key,
            about_me='',
            options='',
            last_login=int(time.time()),
            invited_by=invited_by,
            invite_code=invite_code
        ))
        db.session.commit()


def change_user_details(username, password, options):
    user = User.query.filter_by(username=username).first()
    user.password = password
    user.options = options
    db.session.commit()


def update_last_login_on_user(username):
    user = User.query.filter_by(username=username).first()
    user.last_login = int(time.time())
    db.session.commit()


def does_user_exist(username):
    return True if User.query.with_entities(User.username).filter_by(username=username).first() is not None else False


def add_vote_to_post(post_id, username):
    post = Post.query.filter_by(id=post_id).first()
    post.votes = f"{post.votes};{username}"
    post.updated = int(time.time())
    db.session.commit()


def get_votes_on_post(post_id):
    return Post.query.with_entities(Post.votes).filter_by(id=post_id).first().votes.split(';')


def get_datetime_on_post(post_id):
    return Post.query.with_entities(Post.datetime).filter_by(id=post_id).first().datetime


def add_report_to_post(post_id, username):
    post = Post.query.filter_by(id=post_id).first()
    post.reports = f"{post.reports};{username}"
    db.session.commit()


def get_reports_on_post(post_id):
    return Post.query.with_entities(Post.reports).filter_by(id=post_id).first().reports.split(';')


def insert_post(username, title, url, tags):
    db.session.add(Post(
        title=title,
        url=url,
        username=username,
        datetime=int(time.time()),
        tags=tags,
        votes=username,
        reports='0',
        updated=int(time.time())
    ))
    db.session.commit()


def delete_post(post_id, username):
    Post.query.filter_by(id=post_id, username=username).delete()
    db.session.commit()


def get_post(post_id):
    return Post.query.filter_by(id=post_id).first()


def edit_post(post_id, title, url, tags):
    post = Post.query.filter_by(id=post_id).first()
    post.title = title
    post.url = url
    post.tags = tags
    post.updated = int(time.time())
    db.session.commit()


def get_all_user_details(username):
    return User.query.filter_by(username=username).first()


def get_all_user_invitee():
    return User.query.with_entities(User.username, User.invited_by)


def get_tag_count():
    from core.function import list_of_tags
    count = {}
    for t in list_of_tags():
        count[t] = Post.query.with_entities(Post.tags).filter_by(tags=t).count()
    return count


def get_user_post_points(username):
    total = 0
    for p in Post.query.with_entities(Post.votes).filter_by(username=username).all():
        total += len(p.votes.split(';'))
    return total


def get_user_post_count(username):
    return len(Post.query.with_entities(Post.id).filter_by(username=username).all())


def get_user_by_invite_code(invite_code):
    return User.query.with_entities(User.username, User.invite_code).filter_by(invite_code=invite_code).first()


def get_all_posts(page, num=10):
    return Post.query.order_by(desc('datetime')).paginate(page=page, per_page=num)


def get_all_posts_with_tag(tag, page, num=10):
    return Post.query.filter_by(tags=tag).order_by(desc('datetime')).paginate(page=page, per_page=num)


def get_all_recent_updated_posts(user=None):
    if user is None:
        return Post.query.order_by(desc('updated')).limit(5).all()
    else:
        return Post.query.filter_by(username=user).order_by(desc('updated')).limit(5).all()


def get_all_posts_for_rss():
    return Post.query.order_by(desc('datetime')).limit(10).all()


def get_all_user_posts_for_rss(user):
    return Post.query.filter_by(username=user).order_by(desc('datetime')).limit(10).all()


def get_all_top_posts(user=None):
    votes, top = {}, []
    if user is None:
        for p in Post.query.all():
            votes[p.id] = len(p.votes.split(';'))
    else:
        for p in Post.query.filter_by(username=user).all():
            votes[p.id] = len(p.votes.split(';'))
    for p in list(sorted(votes, key=votes.get, reverse=True))[0:5]:
        top.append(get_post(p))
    return top


def search_for_posts(page, query, search_type):
    if search_type == 'tag':
        query = Post.tags.like(f'%{query}%')

    if search_type == 'domain':
        query = Post.url.like(f'%{query}%')

    if search_type == 'user':
        query = Post.username.like(f'%{query}%')

    if search_type == 'title':
        query = Post.title.like(f'%{query}%')

    total = len(Post.query.filter(query).all())
    results = Post.query.filter(query).order_by(desc('updated')).paginate(page=page, per_page=5)

    return total, results


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    about_me = db.Column(db.Text, nullable=True)
    options = db.Column(db.Text, nullable=True)
    last_login = db.Column(db.Integer, nullable=False)
    invited_by = db.Column(db.Text, nullable=False)
    invite_code = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<User: id={0.id!r},username={0.username!r},password={0.password!r},private_key={0.private_key!r},' \
               'about_me={0.about_me!r},options={0.options!r},last_login={0.last_login!r},' \
               'invited_by={0.invited_by!r},invite_code={0.invite_code!r}>'.format(self)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(16), nullable=False)
    datetime = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.Text, nullable=False)
    votes = db.Column(db.Text, nullable=False)
    reports = db.Column(db.Text, nullable=False)
    updated = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Post: id={0.id!r},title={0.title!r},url={0.url!r},username={0.username!r},datetime={0.datetime!r},' \
               'tags={0.tags!r},votes={0.votes!r},reports={0.reports!r},updated={0.updated!r}>'.format(self)


def init():
    if not os.path.isfile(f"/{get_config_value('database')}"):
        db.create_all()
        db.session.commit()
        db_superuser = get_config_value('superuser')
        su_username = db_superuser['username']
        su_invite_code = db_superuser['invite_code']
        insert_user(su_username, '0', '0', 'overseer', su_invite_code)
        db.session.commit()
