import os

from flask import make_response, abort
from flask import render_template, send_from_directory

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
REST API
"""


@app.route('/api/<param>')
def create_stream(param):
    return param
    return make_response("what")
    # TODO
    abort(404)


"""
Error Handling
"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
