from flask import render_template, send_from_directory, Blueprint, url_for, session, redirect

from core.function import init_session

router = Blueprint('route', __name__)


@router.route('/favicon.ico')
def favicon():
    return send_from_directory('/static/img', 'logo.png')


@router.route('/up/<post_id>')
def upvote(post_id=0):
    from routes import post as run
    return run.route('upvote', post_id)


@router.route('/rp/<post_id>')
def report(post_id=0):
    from routes import post as run
    return run.route('report', post_id)


@router.route('/rm/<post_id>')
def remove(post_id=0):
    from routes import post as run
    return run.route('delete', post_id)


@router.route('/pw/', methods=['GET', 'POST'])
def change_password():
    from routes import password as run
    return run.route()


@router.route('/')
def index():
    from routes import index as run
    return run.route()


@router.route('/l/', methods=['GET', 'POST'])
def login():
    from routes import login as run
    return run.route()


@router.route('/o/')
def logout():
    keep_view = session['view_mode']
    session.clear()
    session['view_mode'] = keep_view
    return redirect(url_for('route.index'))


@router.route('/i/')
@router.route('/i/<code>', methods=['GET', 'POST'])
def invite(code=None):
    from routes import invite as run
    return run.route(code)


@router.route('/f/', methods=['GET', 'POST'])
def forgot():
    from routes import forgot as run
    return run.route()


@router.route('/m/', methods=['GET', 'POST'])
@router.route('/m/edit/<post_id>', methods=['GET', 'POST'])
def submit(post_id=None):
    from routes import submit as run
    return run.route(post_id)


@router.route('/g/')
@router.route('/g/<tag>')
def tags(tag=None):
    if not tag:
        from core.database import get_tag_count
        return render_template(f'{session["view_mode"]}/tags.html', tag_count=get_tag_count())
    else:
        from routes import tag as run
        return run.route(tag)


@router.route('/s/', methods=['GET'])
def search():
    from routes import search as run
    return run.route()


@router.route('/u/')
@router.route('/u/<viewuser>')
def user(viewuser=None):
    from routes import user as run
    return run.route(viewuser)


@router.route('/d/')
@router.route('/d/<domain_urls>')
def domains():
    return render_template(f'{session["view_mode"]}/domains.html')


@router.route('/a/')
def about():
    return render_template(f'{session["view_mode"]}/about.html')


@router.route('/r/')
def recent():
    from routes import toprecent as run
    from core.database import get_all_recent_updated_posts
    return run.route(get_all_recent_updated_posts(), 'recent')


@router.route('/t/')
def top():
    from routes import toprecent as run
    from core.database import get_all_top_posts
    return run.route(get_all_top_posts(), 'top')


@router.route('/b/')
@router.route('/b/<viewuser>')
def subscribe(viewuser=None):
    from routes import rss as run
    return run.route(viewuser)


@router.route('/v/')
def change_view():
    init_session()
    session['view_mode'] = 'mobile' if session['view_mode'] == 'desktop' else 'desktop'
    return redirect(url_for('route.index'))
