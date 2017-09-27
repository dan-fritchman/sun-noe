from flask import Flask, render_template

from sheet import GoogleDocBackend

back_end = GoogleDocBackend()
app = Flask(__name__)


@app.route('/')
@app.route('/status')
def status():
    r = back_end.sheet.get_all_records()
    return str(r)


@app.route('/<name>')
def player_page(name):
    return f'how about a status {name}?'


@app.route('/<name>/<status>')
def update(name, status):
    # Load up status
    str_stat = str(status).lower()

    if str_stat in 'in yes '.split():
        back_end.update_status(id=name, status='In')
        return render_template('response.html', STATUS='IN', REPLY='Got it. See you Sunday.')
    elif str_stat in 'out no '.split():
        back_end.update_status(id=name, status='Out')
        return render_template('response.html', STATUS='OUT', REPLY='Aight. Catch you next time.')
    elif str_stat in 'tbd '.split():
        back_end.update_status(id=name, status='TBD')
        return render_template('response.html', STATUS='TBD', REPLY='OK, keep us posted later this week.')
    else:
        return f'SORRY didnt really understand {str_stat}'


if __name__ == '__main__':
    app.run()
