import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDocBackend(object):
    sheet_name = 'Sunday Noe Bball'
    expected_cols = 'Name ID Phone Sunday Quarter '.split()

    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds']
        j = json.loads(os.environ['GSPREAD_JSON'])
        print(j)
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

    def update_status(self, id, status):
        ids = self.sheet.col_values(col=self.column(name='ID'))
        if id in ids:
            r = ids.index(id) + 1
            c = self.column(name='Sunday')
            self.sheet.update_cell(row=r, col=c, val=status)


if __name__ == '__main__':
    GoogleDocBackend()
