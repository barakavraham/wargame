import functools
import os
import flask
import google.oauth2.credentials
import googleapiclient.discovery
from app import db
from app.models import User
from dotenv import load_dotenv
from authlib.client import OAuth2Session
from flask_login import login_user, current_user
from flask import url_for

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE ='openid email profile'

load_dotenv()

AUTH_REDIRECT_URI = os.getenv("FN_AUTH_REDIRECT_URI")
BASE_URI = os.getenv("FN_BASE_URI")
CLIENT_ID = os.getenv("FN_CLIENT_ID")
CLIENT_SECRET = os.getenv("FN_CLIENT_SECRET")

AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'

google_auth = flask.Blueprint('google_auth', __name__, template_folder='templates')


def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False


def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]
    
    return google.oauth2.credentials.Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)


def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)

    return oauth2_client.userinfo().get().execute()


def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)


@google_auth.route('/login')
@no_cache
def login():
    if current_user.is_authenticated:
        return flask.redirect(url_for('base.index'))
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)

    uri, state = session.authorization_url(AUTHORIZATION_URL)

    flask.session[AUTH_STATE_KEY] = state
    flask.session.permanent = True
    return flask.redirect(uri, code=302)


@google_auth.route('/auth')
@no_cache
def google_auth_redirect():
    if current_user.is_authenticated:
        return flask.redirect(url_for('base.index'))
    req_state = flask.request.args.get('state', default=None, type=None)

    if req_state != flask.session[AUTH_STATE_KEY]:
        return flask.make_response('Invalid state parameter', 401)
    
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state=flask.session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
                        ACCESS_TOKEN_URI,            
                        authorization_response=flask.request.url)

    flask.session[AUTH_TOKEN_KEY] = oauth2_tokens

    google_user = get_user_info()
    email = google_user.get('email')
    avatar = google_user.get('picture')

    existing_user = User.query.filter_by(email=email).first()

    if not existing_user:
        user = User(email=email, avatar=avatar, is_google_user=True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
    else:
        login_user(existing_user)

    return flask.redirect(BASE_URI, code=302)


@no_cache
def google_logout():
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)

    return flask.redirect(BASE_URI, code=302)
