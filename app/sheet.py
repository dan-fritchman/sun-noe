import json
import os
from collections import OrderedDict

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDocBackend(object):
    sheet_name = 'Sunday Noe Bball'
    expected_cols = 'Name ID Phone Sunday '.split()
    current_game_col_name = 'Sunday'
    current_qtr_col_name = 'Q4_2018'

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
        """ Return a one-index'ed column #, from column header/ name """
        return self.headers.index(name) + 1

    def col_values(self, name):
        """ Get the column-values in column-name `name` """
        return self.sheet.col_values(col=self.column(name=name))

    @property
    def headers(self):
        """ Get the header-row entries """
        return self.sheet.row_values(1)

    @property
    def ids(self):
        return self.sheet.col_values(col=self.column(name='ID'))

    def update(self, *, id, col, status):
        """ Update Player-id `id`, column `col` to `status` """
        if id not in self.ids:
            raise ValueError

        r = self.ids.index(id) + 1
        c = self.column(name=col)
        self.sheet.update_cell(row=r, col=c, val=status)

    def update_status(self, *, id, status):
        """ Update game-status for ID `id` """
        return self.update(id=id, col=self.current_game_col_name, status=status)

    def update_qtr(self, *, id, status):
        """ Update quarterly status for Player-ID `id`, Quarter `qtr` """
        return self.update(id=id, col=self.current_qtr_col_name, status=status)

    @property
    def df(self):
        """ DataFrame summarizing the fun bits of back-end data """
        do = OrderedDict()
        do['NAME'] = self.col_values('Name')[1:]
        do['ID'] = self.col_values('ID')[1:]
        do['SUNDAY'] = self.col_values('Sunday')[1:]
        do['QUARTER'] = self.col_values('Quarter')[1:]
        df = pd.DataFrame(do)
        return df

    @property
    def html_table(self):
        """ Get an HTML-table, via DataFrame """
        return self.df.to_html(index=False)

    def get_players(self):
        """ Get a list of PlayerStatus structs
        FIXME: can be *a lot* more direct, iterating over rows """

        ids = self.col_values('ID')
        phone_nums = self.col_values('Phone')
        game_sts = self.col_values(self.current_game_col_name)
        qtr_sts = self.col_values(self.current_qtr_col_name)

        assert len(ids) == len(phone_nums)
        assert len(ids) == len(game_sts)
        assert len(ids) == len(qtr_sts)

        players = []

        for _ in range(len(ids)):
            name = ids[_]
            ph = phone_nums[_]
            game = game_sts[_]
            qtr = qtr_sts[_]

            p = PlayerStatus(name=name, phone=ph, game_status=game, qtr_status=qtr)
            players.append(p)

        return players


class PlayerStatus:
    def __init__(self, *, name, phone, game_status, qtr_status):
        self.name = name
        self.phone = phone
        self.game_status = game_status
        self.qtr_status = qtr_status

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, game_status={self.game_status}, qtr_status={self.qtr_status}'

    def valid(self):
        # Check name & phone are valid
        return self.valid_name(self.name) and self.valid_phone(self.phone)

    def pollable(self):
        """ Know how to check for validity and "poll-ability" """
        return self.active() and self.valid()

    def active(self):
        """ Boolean indication of activity for the current quarter """
        # FIXME: some kind of status method
        return self.qtr_status.lower() in ('full', 'half')

    def game_status_known(self):
        return self.game_status.lower() in 'in yes no out '.split()

    @staticmethod
    def valid_phone(phone):
        if not isinstance(phone, str):
            return False
        elif len(phone) != 10:
            return False
        else:
            for c in phone:
                if not c.isdigit():
                    return False
            return True

    @staticmethod
    def valid_name(name):
        return isinstance(name, str) and len(name) > 1


if __name__ == '__main__':
    # For testing connections
    g = GoogleDocBackend()
    for p in g.get_players():
        print(p)
