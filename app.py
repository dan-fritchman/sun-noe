import os

from flask import Flask, render_template, request

from sheet import GoogleDocBackend

back_end = GoogleDocBackend()
app = Flask(__name__)


class Reply(object):
    pass


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


def get_status(str_stat):
    if str_stat in 'in yes '.split():
        return In()
    elif str_stat in 'out no '.split():
        return Out()
    elif str_stat in 'tbd '.split():
        return Tbd()
    else:
        return None


@app.route('/<name>/<status>')
def update(name, status):
    # Sunday status update

    print(f'Status update request for: {name} to {status}')
    str_name = str(name).lower()
    str_stat = str(status).lower()

    if str_name not in back_end.ids:
        return f'SORRY we aint know no {name} '

    sts = get_status(str_stat)
    if sts is None:
        return f'SORRY {name} didnt really understand {str_stat}'

    if back_end.update_status(id=str_name, status=sts.STATUS):
        return render_template('response.html',
                               STATUS=sts.STATUS,
                               REPLY=sts.REPLY,
                               DATA=back_end.html_table)

    return """SORRY something screwed up trying to update yo status. 
                   Maybe do it manually. """


def get_qtr_status(str_stat):
    if str_stat in 'full yes '.split():
        return Full()
    elif str_stat in 'out no '.split():
        return Out()
    elif str_stat in 'half '.split():
        return Half()
    else:
        return None


@app.route('/<name>/quarter/<qname>/<status>')
def update_qtr(name, status, qname='Quarter'):
    print(f'Quarterly status update request for: {name} to {status}')

    str_name = str(name).lower()
    str_stat = str(status).lower()
    str_qname = str(qname)

    if str_name not in back_end.ids:
        return f'SORRY we aint know no {name} '

    sts = get_qtr_status(str_stat)
    if sts is None:
        return f'SORRY {name} didnt really understand {str_stat}'

    if back_end.update_qtr(id=str_name, qtr=str_qname, status=sts.STATUS):
        return render_template('response.html',
                               STATUS=sts.STATUS,
                               REPLY=sts.REPLY,
                               DATA='')

    return """SORRY something screwed up trying to update yo status. 
                       Maybe do it manually. """


@app.route('/poll/<key>')
def poll(key=None):
    """ URL for SMS-based polling """

    # Check they got the secret-key right
    if key != os.environ['POLLING_KEY']:
        return f'Invalid Polling key {key}'

    # Look up the method to use, from request data
    default_method = 'poll_unknowns_sunday'
    meth_name = request.args.get('method', default_method)

    # Look up method from our `msg` module
    import msg
    meth = getattr(msg, meth_name, None)
    if meth is None:
        return f'Invalid polling method: {meth}'

    # Run it!
    rv = meth()

    # And respond with some log-style output
    return '<br>'.join(rv)


if __name__ == '__main__':
    app.run()
