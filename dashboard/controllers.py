import os

from flask import make_response
from flask import render_template
from flask import send_from_directory

import dashboard.api as api
import dashboard.auth as auth
from dashboard import app

"""
Serve the App
"""


# routing for basic pages (pass routing onto the Angular app)
# TODO this is stupid.
@app.route('/')
@app.route('/dashboard')
def basic_pages(*args, **kwargs):
    return make_response(open('dashboard/templates/index.html').read())


"""
Static Files
"""


# special file handlers, the rest is handled by providing the Flask constructor a static path
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


"""
REST API & Auth
"""

auth.register_all(app)
api.register_all(app)

"""
Error Handling
"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
