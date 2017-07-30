import os
from dashboard import app


def run():
    # Start the dashboard app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # TODO do more here

if __name__ == '__main__':
    run()
