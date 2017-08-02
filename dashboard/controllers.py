import os

from flask import g, session, request, url_for, flash
from flask import make_response, abort
from flask import redirect, render_template
from flask import send_from_directory
from flask_oauthlib.client import OAuth

from dashboard import app

"""
Serve the App
"""


# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
def basic_pages(**kwargs):
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


import dashboard.api
import dashboard.auth

"""
Error Handling
"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
