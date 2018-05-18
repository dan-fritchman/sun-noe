import json
import os
from collections import OrderedDict

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDocBackend(object):
    sheet_name = 'Sunday Noe Bball'
    expected_cols = 'Name ID Phone Sunday '.split()

    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds']
        js = os.environ['GSPREAD_JSON']
        j = json.loads(js)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(j, scope)
        client = gspread.authorize(creds)

        # Load up the sheet
        self.sheet = client.open(self.sheet_name).sheet1
        # Check for required columns
        for x in self.expected_cols:
            if x not in self.headers:
                raise ValueError(f'Did not find required column: {x}')

    def column(self, name):
        # Return a one-index'ed column #, from column header/ name
        return self.headers.index(name) + 1

    def col_values(self, name):
        return self.sheet.col_values(col=self.column(name=name))

    @property
    def headers(self):
        return self.sheet.row_values(1)

    @property
    def ids(self):
        return self.sheet.col_values(col=self.column(name='ID'))

    def update_status(self, id, status):
        # Update Sunday status for ID <id>

        if id not in self.ids:
            return False

        r = self.ids.index(id) + 1
        c = self.column(name='Sunday')
        self.sheet.update_cell(row=r, col=c, val=status)
        return True

    def update_qtr(self, id, qtr, status):
        # Update quarterly status for ID <id>, Quarter <qtr>

        if qtr not in self.headers:
            return False
        if id not in self.ids:
            return False

        r = self.ids.index(id) + 1
        c = self.column(name=qtr)
        self.sheet.update_cell(row=r, col=c, val=status)
        return True

    @property
    def df(self):
        # DataFrame summarizing the fun bits of back-end data.
        do = OrderedDict()
        do['NAME'] = self.col_values('Name')[1:]
        do['ID'] = self.col_values('ID')[1:]
        do['SUNDAY'] = self.col_values('Sunday')[1:]
        do['QUARTER'] = self.col_values('Quarter')[1:]
        df = pd.DataFrame(do)
        return df

    @property
    def html_table(self):
        return self.df.to_html(index=False)


if __name__ == '__main__':
    # For testing connections
    GoogleDocBackend()
