"""
Main Flask App

Including creation of the Flask instance,
and all of our routes/ endpoints.
"""

from flask import Flask, render_template, request

from . import config
from .sheet import GoogleDocBackend

back_end = GoogleDocBackend()
app = Flask(__name__)


@app.route('/')
@app.route('/status')
def status_table():
    return back_end.html_table


@app.route('/<name>/<status>')
def update(name, status):
    """ Game-status update """

    print(f'Status update request for: {name} to {status}')
    str_name = str(name).lower()
    str_stat = str(status).lower()

    if str_name not in back_end.ids:
        return f'SORRY we aint know no {name} '

    from .models import GameStatus
    sts = GameStatus.from_str(str_stat)
    if not sts.valid():
        return f'SORRY {name} didnt really understand {str_stat}'

    try:
        back_end.update_game_status(id=str_name, status=sts.STATUS)
    except Exception as e:
        print(e)
        return """SORRY something screwed up trying to update yo status. Maybe do it manually. """
    else:
        return render_template('response.html',
                               STATUS=sts.STATUS,
                               REPLY=sts.REPLY,
                               DATA=back_end.html_table)


@app.route('/poll/<key>')
def poll(key=None):
    """ URL-based invocation of SMS polling """

    # Check they got the secret-key right
    if key != config.polling_key:
        return f'Invalid Polling key {key}'

    try:  # Look up the method to use, from request data
        meth_name = request.args.get('method', None)
        from .msg import get_polling_method
        meth = get_polling_method(meth_name)
        assert callable(meth)
    except:
        return f'Invalid polling method: {meth}'

    # Run it in the background
    from threading import Thread
    Thread(target=meth).start()

    # And respond with some log-style output
    return f'Running {meth.__name__}', 200
