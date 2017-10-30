from flask import Flask, render_template

from sheet import GoogleDocBackend

back_end = GoogleDocBackend()
app = Flask(__name__)


@app.route('/')
@app.route('/status')
def status():
    return back_end.html_table


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
    # Load up status
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
    else:
        return """SORRY something screwed up trying to update yo status. 
                   Maybe do it manually. """


if __name__ == '__main__':
    app.run()
