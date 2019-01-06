import sys
from flask import Flask, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from db_config import Base, Category, Item, User
from flask import session as login_session
import random
import string

app = Flask(__name__)
app.secret_key = 'super_secret_key'
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))


def generate_csrf_token():
    if '_csrf_token' not in login_session:
        login_session['_csrf_token'] = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for x in range(128))
    return login_session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


from core import app_setup
from core import oauth

if __name__ == "__main__":
    # Only for debugging while developing
    app.debug = True
    app.run(host='0.0.0.0', debug=True, port=8000, ssl_context='adhoc')
