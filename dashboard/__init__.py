from flask import Flask
from flask_socketio import SocketIO

# Initialize the app
app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

# Create the config
app.config.from_object('dashboard.settings')
app.url_map.strict_slashes = False


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


# Initialize controllers and core TODO there has to be a better way
import dashboard.controllers
import dashboard.core
