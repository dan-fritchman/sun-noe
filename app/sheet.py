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
        # use creds to create a client to interact with the Google Drive API
        ##scope = ['https://spreadsheets.google.com/feeds']
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
        records = self.sheet.get_all_records()
        players = []
        for r in records:
            p = PlayerStatus(name=str(r['ID']),
                             phone=str(r['Phone']),
                             game_status=str(r[self.current_game_col_name]),
                             qtr_status=str(r[self.current_qtr_col_name]))
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


class PlayerStatus:
    """ PlayerStatus
    Generally represents a `row` in the back-end, including:
    * Player id info (name, contact, etc)
    * Status for key ongoing events (current game, current quarter) """

    def __init__(self, *, name: str, phone: str, game_status: str, qtr_status: str):
        self.name = name.strip()
        self.phone = phone.strip()
        self.game_status = game_status.strip()
        self.qtr_status = qtr_status.strip()

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, phone={self.phone}, game_status={self.game_status}, qtr_status={self.qtr_status}'

    def valid(self):
        """ Check name & phone are valid """
        return self.valid_name() and self.valid_phone()

    def pollable(self):
        """ Know how to check for validity and "poll-ability" """
        return self.active() and self.valid()

    def active(self):
        """ Boolean indication of activity for the current quarter """
        # FIXME: some kind of status method
        return self.qtr_status.lower() in ('full', 'half')

    def game_status_known(self):
        # FIXME: should be a more central idea of known/ unknown
        return self.game_status.lower() in 'in yes no out '.split()

    def valid_phone(self):
        """ Test phone validity.  *Only* accepts ten-digit strings (no punctuation). """
        phone = self.phone
        if not isinstance(phone, str):
            ##warnings.warn(f'Non-string phone: {self}')
            return False
        elif len(phone) != 10:
            ##warnings.warn(f'Wrong-length phone: {self}, length {len(self.phone)}')
            return False
        else:
            for c in phone:
                if not c.isdigit():
                    ##warnings.warn(f'Non-digit in phone: {self}')
                    return False
            return True

    def valid_name(self):
        """ Test name (id) validity.  Really just a string-length test. """
        name = self.name
        return isinstance(name, str) and len(name) > 1
