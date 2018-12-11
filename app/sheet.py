"""
Google Sheets manipulation, as a sort of database client.
"""

import json

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from . import config


class GoogleDocBackend(object):
    """ "Client" for our Google-Sheet-based "player database". """

    sheet_name = 'Sunday Noe Bball'
    game_col_name = 'Sunday'
    qtr_col_name = 'Q4_2018'
    required_cols = ['Name', 'ID', game_col_name, qtr_col_name]

    def __init__(self):
        # Create a Google Drive API client
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        js = config.gspread_json
        j = json.loads(js)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(j, scope)
        client = gspread.authorize(creds)

        # Load up the sheet
        self.url = config.gspread_url
        self.sheet = client.open(self.sheet_name).sheet1

        # Check for required columns
        for x in self.required_cols:
            if x not in self.headers:
                raise ValueError(f'Did not find required column: {x}')

    def column(self, name: str):
        """ Return a one-index'ed column #, from column header/ name """
        return self.headers.index(name) + 1

    def col_values(self, name: str):
        """ Get the column-values in column-name `name` """
        return self.sheet.col_values(col=self.column(name=name))

    @property
    def headers(self):
        """ Get the header-row entries """
        return self.sheet.row_values(1)

    @property
    def ids(self):
        return self.sheet.col_values(col=self.column(name='ID'))

    def update(self, *, id: str, col: str, status: str):
        """ Update Player-id `id`, column `col` to `status` """
        if id not in self.ids:
            print(f'{self} Cannot Update Unknown ID {id}')
            return None

        r = self.ids.index(id) + 1
        c = self.column(name=col)
        self.sheet.update_cell(row=r, col=c, value=status)

    def update_game_status(self, *, id: str, status: str):
        """ Update game-status for ID `id` """
        return self.update(id=id, col=self.game_col_name, status=status)

    def update_qtr(self, *, id: str, status: str):
        """ Update quarterly status for Player-ID `id`, Quarter `qtr` """
        return self.update(id=id, col=self.qtr_col_name, status=status)

    @property
    def df(self):
        """ DataFrame summarizing the fun bits of back-end data """
        records = self.sheet.get_all_records()
        return pd.DataFrame.from_records(data=records, columns=self.required_cols)

    @property
    def html_table(self):
        """ Get an HTML-table, via DataFrame """
        return self.df.to_html(index=False)

    @property
    def debug_df(self):
        """ DataFrame with much more debug info. """
        players = self.get_players()
        do = dict()
        do['ID'] = [p.name for p in players]
        do['GAME'] = [p.game_status for p in players]
        do['QUARTER'] = [p.qtr_status for p in players]
        do['ACTIVE'] = [p.active() for p in players]
        do['VALID'] = [p.valid() for p in players]
        do['VALID_PHONE'] = [p.valid_phone() for p in players]
        do['VALID_NAME'] = [p.valid_name() for p in players]
        do['POLLABLE'] = [p.pollable() for p in players]
        do['GAME_KNOWN'] = [p.game_status_known() for p in players]
        df = pd.DataFrame(do)
        return df

    def get_players(self):
        """ Returns a list of PlayerStatus structs """
        players = []
        records = self.sheet.get_all_records()
        for r in records:
            r['game'] = r[self.game_col_name]
            r['qtr'] = r[self.qtr_col_name]
            from .models import PlayerStatus
            p = PlayerStatus.from_dict(r)
            if p.valid():
                players.append(p)
        return players

    def get_game_unknowns(self):
        """ Get a list of active Players with unknown status for the upcoming game. """
        players = self.get_players()
        return [p for p in players if p.pollable() and not p.game_status_known()]
