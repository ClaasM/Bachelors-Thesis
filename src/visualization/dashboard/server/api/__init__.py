from server.api.dashboard import dashboard_blueprint

url_prefix = '/api'


def register_all(app):
    app.register_blueprint(dashboard_blueprint, url_prefix=url_prefix + '/dashboard')
