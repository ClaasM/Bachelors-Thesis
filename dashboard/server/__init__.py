from flask import Flask, make_response, send_from_directory
from flask_socketio import SocketIO
import os

# Initialize the app
app = Flask(__name__, static_url_path='/client')
socketio = SocketIO(app)


def start():
    app.url_map.strict_slashes = False

    """
    Serve the App
    """

    # routing for basic pages (pass routing onto the Angular app)
    # TODO this is stupid.
    @app.route('/')
    @app.route('/dashboard')
    def basic_pages(*args, **kwargs):
        return make_response(open('./client/index.html').read())

    """
    Static Files
    """

    # special file handlers, the rest is handled by providing the Flask constructor a static path
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'client'),
                                   'img/favicon.ico')

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
