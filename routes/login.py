import bcrypt
from flask import redirect, render_template, request, url_for, session
from markupsafe import escape

from core.function import init_session
from core.database import get_all_user_details, update_last_login_on_user


def route():
    init_session()
    if request.method == 'POST':
        user_login = get_all_user_details(escape(request.form['username'].lower()))
        if user_login is not None:
            if bcrypt.checkpw(escape(request.form['password']).encode('utf-8'), user_login.password):
                update_last_login_on_user(user_login.username)
                session['logged_in'], session['username'], session['current_page'] = True, user_login.username, 1
                return redirect(url_for('route.index'))
            else:
                return render_template('login.html', error=True)
        else:
            return render_template('login.html', error=True)
    elif request.method == 'GET':
        return render_template('login.html')
    else:
        return redirect(url_for('route.index'))
