import os

from better_profanity import profanity
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from core import database
from core.router import router

server = Flask(__name__)

server.register_blueprint(router)

server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

server.secret_key = os.urandom(32)

db = SQLAlchemy(server)


@server.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=f'{error.code} {error.name}')


if __name__ == '__main__':
    profanity.load_censor_words()
    database.init()
    server.run(debug=True, host="127.0.0.1", port="3000")
    # server.run(debug=True, host="0.0.0.0", port="3000")
    # serve(server, host='0.0.0.0', port=3000, url_scheme='https', threads=10)
