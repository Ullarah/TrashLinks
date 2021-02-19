import bcrypt
from flask import render_template, redirect, request, session, url_for
from markupsafe import escape

from app import init_session
from database import get_all_user_details, change_user_details


def route():
    init_session()
    if request.method == 'POST':
        username = request.form['username'].lower()
        if len(request.form['password'].lower()) < 8:
            session['short_password'] = True
            return redirect(f'/u/{username}')
        if session['logged_in'] and username == escape(session['username']):
            if get_all_user_details(username) is not None:
                password = bcrypt.hashpw(escape(request.form['password']).encode('utf-8'), bcrypt.gensalt(16))
                options = ';'
                change_user_details(username, password, options)
                session.clear()
                return render_template('private.html', password_changed=True, type=f'Password Changed for {username}')
    return redirect(url_for('index'))
