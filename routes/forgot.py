import bcrypt
from flask import redirect, render_template, request, session, url_for
from markupsafe import escape

from core.function import init_session
from core.database import get_all_user_details, change_user_details


def route():
    init_session()
    if request.method == 'POST':
        username = request.form['username'].lower()
        user_login = get_all_user_details(escape(username))
        if user_login is not None:
            if bcrypt.checkpw(escape(request.form['private_key']).encode('utf-8'), user_login.private_key):
                password = request.form['password']
                if len(password) < 8:
                    return render_template(f'{session["view_mode"]}/forgot.html', short_password=True)
                password = bcrypt.hashpw(escape(password).encode('utf-8'), bcrypt.gensalt(16))
                options = ';'
                change_user_details(user_login.username, password, options)
                return render_template(f'{session["view_mode"]}/private.html',
                                       user_recovered=True, type=f'Account recovered for {username}')
        else:
            return render_template(f'{session["view_mode"]}/forgot.html', invalid_private_key=True)
    elif request.method == 'GET':
        if session['logged_in']:
            return redirect(url_for('route.index'))
        return render_template(f'{session["view_mode"]}/forgot.html')
    else:
        return redirect(url_for('route.index'))
