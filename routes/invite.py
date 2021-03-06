import bcrypt
from better_profanity import profanity
from flask import redirect, render_template, request, url_for, session
from markupsafe import escape
from random_word import RandomWords

from core.function import generate_code, init_session
from core.database import does_user_exist, get_user_by_invite_code, insert_user


def route(code):
    init_session()
    if request.method == 'POST':
        user_invite = get_user_by_invite_code(code)
        if does_user_exist(request.form['username'].lower()):
            return render_template(f'{session["view_mode"]}/invite.html',
                                   invite_from=user_invite.username,
                                   invite_code=code,
                                   user_exists=True)
        if len(request.form['username'].lower()) < 4:
            return render_template(f'{session["view_mode"]}/invite.html',
                                   invite_from=user_invite.username,
                                   invite_code=code,
                                   less_than_four=True)
        if len(request.form['username'].lower()) > 16:
            return render_template(f'{session["view_mode"]}/invite.html',
                                   invite_from=user_invite.username,
                                   invite_code=code,
                                   more_than_sixteen=True)
        if len(request.form['password'].lower()) < 8:
            return render_template(f'{session["view_mode"]}/invite.html',
                                   invite_from=user_invite.username,
                                   invite_code=code,
                                   short_password=True)
        if request.form['username'].lower() in [
            'admin', 'administrator', 'root', 'system', 'qanon', '4chan', 'quisquiliae', 'user', 'username',
            'hitler', 'jesus', 'stalin', 'trump', 'phil', 'overseer', 'rocketotter'
        ] or profanity.contains_profanity(request.form['username'].lower()):
            return render_template(f'{session["view_mode"]}/invite.html',
                                   invite_from=user_invite.username,
                                   invite_code=code,
                                   blacklisted=True)
        invited_by = get_user_by_invite_code(request.form['invite_code'])
        private_key = []
        for i in range(4):
            private_key.append(RandomWords().get_random_word(minLength=4, maxLength=8, includePartOfSpeech="verb"))
        private_key_raw = '-'.join(private_key).lower()
        private_key = bcrypt.hashpw(escape('-'.join(private_key).lower()).encode('utf-8'), bcrypt.gensalt(16))
        invite_code = generate_code(32)
        insert_user(escape(request.form['username'].lower()),
                    bcrypt.hashpw(escape(request.form['password']).encode('utf-8'), bcrypt.gensalt(16)),
                    private_key=private_key, invited_by=invited_by.username, invite_code=invite_code)
        return render_template(f'{session["view_mode"]}/private.html',
                               user_created=True,
                               private_key=private_key_raw,
                               user=escape(request.form['username'].lower()))
    elif request.method == 'GET':
        if code is None:
            return redirect(url_for('route.index'))
        user_invite = get_user_by_invite_code(code)
        if user_invite is not None:
            return render_template(f'{session["view_mode"]}/invite.html',
                                   invalid_invite_code=False,
                                   invite_from=user_invite.username,
                                   invite_code=code,
                                   valid_invite_code=True)
        else:
            return render_template(f'{session["view_mode"]}/invite.html',
                                   invalid_invite_code=True)
    else:
        return redirect(url_for('route.index'))
