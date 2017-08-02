from flask import redirect, session, request, url_for, flash, Blueprint

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/sync')
def sync():
    if 'twitter_oauth' not in session:
        return redirect(url_for('login', next=request.url))
    status = request.form['tweet']
    if not status:
        return redirect(url_for('index'))
    resp = "Bla"

    if resp.status == 403:
        flash("Error: #%d, %s " % (
            resp.data.get('errors')[0].get('code'),
            resp.data.get('errors')[0].get('message'))
              )
    elif resp.status == 401:
        flash('Authorization error with Twitter.')
    else:
        flash('Successfully tweeted your tweet (ID: #%s)' % resp.data['id'])
    return redirect(url_for('index'))
