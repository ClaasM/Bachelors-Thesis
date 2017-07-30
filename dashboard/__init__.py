from flask import Flask

# Initialize the app
app = Flask(__name__, static_url_path='/static')

# Create the config
app.config.from_object('dashboard.settings')

app.url_map.strict_slashes = False

# Initialize controllers and core TODO there has to be a better way
import dashboard.controllers
import dashboard.core
