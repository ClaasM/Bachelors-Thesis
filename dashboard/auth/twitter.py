import json

import tweepy
from flask import redirect, session, request, url_for, Blueprint

twitter_blueprint = Blueprint('twitter', __name__)

with open('config.json') as config_data:
    config = json.load(config_data)


@twitter_blueprint.route('/login')
def login():
    print(url_for('twitter.callback'))
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'],
                               url_for('twitter.callback', _external=True))
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)


@twitter_blueprint.route('/callback')
def callback():
    request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)

    print(auth.access_token, auth.access_token_secret)

    session['token'] = (auth.access_token, auth.access_token_secret)

    return redirect('/dashboard')
