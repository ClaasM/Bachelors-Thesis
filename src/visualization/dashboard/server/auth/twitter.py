import json

import tweepy
from flask import redirect, session, request, url_for, Blueprint

twitter_blueprint = Blueprint('twitter', __name__)

with open('../../../twitter.access.json') as access_info_file:
    access_info = json.load(access_info_file)


@twitter_blueprint.route('/login')
def login():
    auth = tweepy.OAuthHandler(access_info['consumer_key'], access_info['consumer_secret'],
                               url_for('twitter.callback', _external=True))
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)


@twitter_blueprint.route('/callback')
def callback():
    print(request.args)

    request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(access_info['consumer_key'], access_info['consumer_secret'])
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)

    print(auth.access_token, auth.access_token_secret)

    session['token'] = (auth.access_token, auth.access_token_secret)

    return redirect('/dashboard')
