import argparse
import os

from better_profanity import profanity
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from waitress import serve

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

    parser = argparse.ArgumentParser(prog='trash-links')

    parser.add_argument('-d', type=bool, choices=[True, False], default=False, dest='debug', help='debug mode')
    parser.add_argument('-o', type=str, default='0.0.0.0', dest='host', help='serving ip address')
    parser.add_argument('-p', type=int, default=3000, dest='port', help='port to use')
    parser.add_argument('-t', type=int, default=10, dest='threads', help='number of server threads')

    args = parser.parse_args()

    if args.debug:
        server.run(debug=True, host=args.host, port=args.port)
    else:
        serve(server, host=args.host, port=args.port, url_scheme='https', threads=args.threads)
