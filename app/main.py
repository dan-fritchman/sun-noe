"""
Main Flask App

Including creation of the Flask instance,
and all of our routes/ endpoints.
"""
import os
from threading import Thread

from flask import Flask, render_template, request

from .sheet import GoogleDocBackend

back_end = GoogleDocBackend()
app = Flask(__name__)


class Reply(object):
    @staticmethod
    def from_str(str_stat):
        if str_stat in 'in yes '.split():
            return In()
        elif str_stat in 'out no '.split():
            return Out()
        elif str_stat in 'tbd '.split():
            return Tbd()
        return None


class In(Reply):
    STATUS = 'IN'
    REPLY = 'Got it. See you Sunday.'


class Out(Reply):
    STATUS = 'OUT'
    REPLY = 'Aight. Catch you next time.'


class Tbd(Reply):
    STATUS = 'TBD'
    REPLY = 'OK, keep us posted later this week.'


class Full(Reply):
    STATUS = 'FULL'
    REPLY = 'Got it.'


class Half(Reply):
    STATUS = 'HALF'
    REPLY = 'Aight, well see you half time.'


@app.route('/')
@app.route('/status')
def status():
    return back_end.html_table


@app.route('/<name>/<status>')
def update(name, status):
    """ Game-status update """

    print(f'Status update request for: {name} to {status}')
    str_name = str(name).lower()
    str_stat = str(status).lower()

    if str_name not in back_end.ids:
        return f'SORRY we aint know no {name} '

    sts = Reply.from_str(str_stat)
    if sts is None:
        return f'SORRY {name} didnt really understand {str_stat}'

    try:
        back_end.update_status(id=str_name, status=sts.STATUS)
    except:
        return """SORRY something screwed up trying to update yo status. 
                           Maybe do it manually. """
    else:
        return render_template('response.html',
                               STATUS=sts.STATUS,
                               REPLY=sts.REPLY,
                               DATA=back_end.html_table)


@app.route('/poll/<key>')
def poll(key=None):
    """ URL for SMS-based polling """

    # Check they got the secret-key right
    if key != os.environ['POLLING_KEY']:
        return f'Invalid Polling key {key}'

    try:  # Look up the method to use, from request data
        from .msg import get_polling_method
        meth_name = request.args.get('method', None)
        meth = get_polling_method(meth_name)
        assert callable(meth)
    except:
        return f'Invalid polling method: {meth}'

    # Run it in the background
    Thread(target=meth).start()
    # And respond with some log-style output
    return f'Running {meth.__name__}', 200


if __name__ == '__main__':
    app.run()
