from enum import IntEnum, auto

from flask import Flask, url_for

app = Flask(__name__)


class Player(object):
    pass


class PlayerStatus(IntEnum):
    Unknown = auto()
    Tbd = auto()
    Out = auto()
    In = auto()


class BackEnd(object):
    # Base class for whatever eventually stores attendance data.
    pass


class JustDanBackEnd(BackEnd):
    # In-memory, single-player version of the back-end, mostly for screwing around and testing.
    def __init__(self):
        self.name = 'Dan'
        self.num = '6102488063'
        self.status = PlayerStatus.Unknown


back_end = JustDanBackEnd()


@app.route('/')
@app.route('/status')
def status():
    return f'name : {back_end.name}, status : {str(back_end.status)}'


@app.route('/send')
def send():
    return 'send it in'

@app.route('/<name>')
def player_page(name):
    return f'how about a status {name}?'


@app.route('/<name>/<status>')
def update(name, status):
    if False: # check for names
        pass

    # Load up status
    str_stat = str(status).lower()

    if str_stat in 'in yes '.split():
        s = PlayerStatus.In
        back_end.status = s
        return 'GOT IT. See you Sunday.'
    elif str_stat in 'out no '.split():
        s = PlayerStatus.Out
        back_end.status = s
        return 'AIGHT. Catch you next time.'
    elif str_stat in 'tbd '.split():
        s = PlayerStatus.Tbd
        back_end.status = s
        return 'OK, keep us posted later this week'
    else:
        s = PlayerStatus.Unknown
        back_end.status = s
        x = 'http://127.0.0.1:5000' + url_for('update', name=name, status="in")
        return f'sorry didnt really understand {str_stat}, {x}'




if __name__ == '__main__':
    app.run()
