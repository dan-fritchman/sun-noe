import json

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from . import config


class GoogleDocBackend(object):
    """ "Client" for our Google-Sheet-based "player database". """

    sheet_name = 'Sunday Noe Bball'
    expected_cols = 'Name ID Phone Sunday '.split()
    current_game_col_name = 'Sunday'
    current_qtr_col_name = 'Q4_2018'

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

    def update(self, *, id: str, col: str, status: str):
        """ Update Player-id `id`, column `col` to `status` """
        if id not in self.ids:
            print(f'{self} Cannot Update Unknown ID {id}')
            return None

        r = self.ids.index(id) + 1
        c = self.column(name=col)
        self.sheet.update_cell(row=r, col=c, val=status)

    def update_status(self, *, id: str, status: str):
        """ Update game-status for ID `id` """
        return self.update(id=id, col=self.current_game_col_name, status=status)

    def update_qtr(self, *, id: str, status: str):
        """ Update quarterly status for Player-ID `id`, Quarter `qtr` """
        return self.update(id=id, col=self.current_qtr_col_name, status=status)

    @property
    def df(self):
        """ DataFrame summarizing the fun bits of back-end data """
        do = dict()
        do['NAME'] = self.col_values('Name')[1:]
        do['ID'] = self.col_values('ID')[1:]
        do['SUNDAY'] = self.col_values('Sunday')[1:]
        do['QUARTER'] = self.col_values('Quarter')[1:]
        df = pd.DataFrame(do)
        return df

    @property
    def debug_df(self):
        """ DataFrame summarizing the fun bits of back-end data """
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

    @property
    def html_table(self):
        """ Get an HTML-table, via DataFrame """
        return self.df.to_html(index=False)

    def get_players(self):
        """ Get a list of PlayerStatus structs """
        players = []
        records = self.sheet.get_all_records()
        for r in records:
            p = self.get_player_status(r)
            if p.valid():
                players.append(p)
                print(f'Adding Valid Player {p}')
            else:
                print(f'Not Adding Invalid Player {p}')
        return players

    def get_game_uknowns(self):
        """ Get a list of active Players with unknown status for the upcoming game. """
        players = self.get_players()
        return [p for p in players if p.pollable() and not p.game_status_known()]

    def get_player_status(self, r: dict):
        """ Get a PlayerStatus from dictionary-record `r`. """
        r['game'] = r[self.current_game_col_name]
        r['qtr'] = r[self.current_qtr_col_name]
        from .models import PlayerStatus
        return PlayerStatus.from_dict(r)
