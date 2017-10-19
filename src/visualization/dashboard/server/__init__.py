import mimetypes

from flask import Flask, make_response, send_from_directory
from flask_socketio import SocketIO
from werkzeug.exceptions import NotFound
import os

# Initialize the app
app = Flask(__name__, static_folder="../client")
socketio = SocketIO(app)


def start():
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.config.from_object('server.settings')
    app.url_map.strict_slashes = False

    """
    Serve the App
    """

    # routing for basic pages
    # pass routing onto the Angular app, to enable HTML5Mode (frontend routing without hashbang)
    @app.route('/')
    @app.route('/dashboard')
    def basic_pages(*args, **kwargs):
        return make_response(open('./client/index.html').read())

    @app.route('/<path:path>')
    def send(path):
        try:
            return send_from_directory('../client', path)
        except NotFound:
            return send_from_directory('../.tmp/client', path)
            # if mimetypes.guess_type(path)[0] is None:

    """
    REST API & Auth
    """

    import server.auth as auth
    import server.api as api

    auth.register_all(app)
    api.register_all(app)

    """
    Error Handling
    """

    @app.errorhandler(404)
    def page_not_found(e):
        return "Not found", 404

    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    # Start the dashboard app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
