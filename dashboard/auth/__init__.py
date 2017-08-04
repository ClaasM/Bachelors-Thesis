from dashboard.auth.twitter import twitter_blueprint

url_prefix = '/auth'


def register_all(app):
    app.register_blueprint(twitter_blueprint, url_prefix=url_prefix)
