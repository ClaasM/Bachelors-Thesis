from flask import redirect, session, request, url_for, Blueprint

from flask_oauthlib.client import OAuth

from dashboard import app

twitter_blueprint = Blueprint('twitter', __name__)

twitter_oauth = OAuth(app).remote_app(
    'twitter',
    consumer_key='xBeXxg9lyElUgwZT6AZ0A',
    consumer_secret='aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)


@twitter_blueprint.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter_oauth.authorize(callback=callback_url or request.referrer or None)


@twitter_blueprint.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('index'))


@twitter_blueprint.route('/oauthorized')
def oauthorized():
    resp = twitter_oauth.authorized_response()
    if resp is None:
        print('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect('/dashboard')


# TODO is this needed?
@twitter_oauth.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']
