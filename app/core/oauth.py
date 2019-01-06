from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import session as login_session
from main import app, DBSession
from flask_oauthlib.client import OAuth
import json

CLIENT_SECRET_FILE = 'client_secrets.json'

GOOGLE_CLIENT_ID = json.loads(
    open(CLIENT_SECRET_FILE, 'r').read())['web']['client_id']
GOOGLE_CLIENT_SECRET = json.loads(
    open(CLIENT_SECRET_FILE, 'r').read())['web']['client_secret']

FB_APP_ID = 
FB_APP_SECRET = 

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET,
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=FB_APP_ID,
    consumer_secret=FB_APP_SECRET,
    request_token_params={
        'scope': 'email'
    },
    request_token_url=None,
    base_url='https://graph.facebook.com',
    access_token_method='POST',
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
)


@app.route('/glogin')
def glogin():
    return google.authorize(callback=url_for('gconnect', _external=True))


@app.route('/gconnect')
def gconnect():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    login_session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    login_session['google_user'] = me.data
    return redirect(url_for('add_user', user_type='google'))


@app.route('/fblogin')
def fblogin():
    return facebook.authorize(callback=url_for('fbconnect', _external=True))


@app.route('/fbconnect')
def fbconnect():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    login_session['facebook_token'] = (resp['access_token'], '')
    me = facebook.get('userinfo')
    login_session['facebook_user'] = me.data
    return jsonify({"data": me.data})
    # return redirect(url_for('add_user', user_type='facebook'))


@google.tokengetter
def get_google_oauth_token():
    return login_session.get('google_token')


@facebook.tokengetter
def get_facebook_oauth_token():
    return login_session.get('facebook_token')
