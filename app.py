from collections import OrderedDict

import pandas as pd
from flask import Flask, render_template

from sheet import GoogleDocBackend

back_end = GoogleDocBackend()
app = Flask(__name__)


def df():
    # DataFrame summarizing the fun bits of back-end data.
    do = OrderedDict()
    do['NAME'] = back_end.col_values('Name')[1:]
    do['ID'] = back_end.col_values('ID')[1:]
    do['SUNDAY'] = back_end.col_values('Sunday')[1:]
    df = pd.DataFrame(do)
    ##df.set_index('NAME', inplace=True)

    return df.to_html(index=False)


@app.route('/')
@app.route('/status')
def status():
    return df()
    ##r = back_end.sheet.get_all_records()
    ##return str(r)


@app.route('/<name>')
def player_page(name):
    return f'how about a status {name}?'


@app.route('/<name>/<status>')
def update(name, status):
    # Load up status
    str_stat = str(status).lower()

    if str_stat in 'in yes '.split():
        back_end.update_status(id=name, status='In')
        return render_template('response.html', STATUS='IN', REPLY='Got it. See you Sunday.', DATA=df())
    elif str_stat in 'out no '.split():
        back_end.update_status(id=name, status='Out')
        return render_template('response.html', STATUS='OUT', REPLY='Aight. Catch you next time.', DATA=df())
    elif str_stat in 'tbd '.split():
        back_end.update_status(id=name, status='TBD')
        return render_template('response.html', STATUS='TBD', REPLY='OK, keep us posted later this week.', DATA=df())
    else:
        return f'SORRY didnt really understand {str_stat}'


if __name__ == '__main__':
    app.run()
