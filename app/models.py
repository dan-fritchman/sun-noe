"""
Player "Database" "Models"
All with plenty of air-quote sarcasm.
A few simple classes to capture the ideas tabulated in-sheet.
"""


class Cell(object):
    """ Roughly, a cell in our spreadsheet back-end. """

    def __init__(self, s):
        self.s = self.format(s)

    @staticmethod
    def format(s):
        x = str(s)
        x = x.strip()
        return x

    def valid(self) -> bool:
        raise NotImplementedError

    def __repr__(self):
        return self.s


class Id(Cell):
    """ Player IDs """

    def valid(self) -> bool:
        return len(self.s) > 1


class Phone(Cell):
    """ Phone Numbers """

    @staticmethod
    def format(s):
        """ More phone-number formatting.  Mostly clear out punctuation. """
        x = Cell.format(s)
        x = x.replace('(', '')
        x = x.replace(')', '')
        x = x.replace('-', '')
        return x

    def valid(self) -> bool:
        """ Test phone validity.  *Only* accepts ten-digit strings (no punctuation). """
        if len(self.s) != 10:
            return False
        return all([c.isdigit() for c in self.s])


class Status(Cell):
    """ Base class for status-replies """

    def __init__(self, s, reply):
        super().__init__(s)
        self.reply = reply


class GameStatus(Status):
    """ Game Reply-Status """

    @staticmethod
    def from_str(str_stat: str):
        if str_stat in 'in yes '.split():
            return In
        elif str_stat in 'out no '.split():
            return Out
        elif str_stat in 'tbd '.split():
            return Tbd
        return Unknown

    def valid(self):
        return bool(len(self.s))

    def known(self):
        return self.s.lower() in 'in yes no out '.split()

    @property
    def STATUS(self):
        return self.s

    @property
    def REPLY(self):
        return self.reply


In = GameStatus(s='IN', reply='Got it. See you Sunday.')
Out = GameStatus(s='OUT', reply='Aight. Catch you next time.')
Tbd = GameStatus(s='TBD', reply='OK, keep us posted later this week.')
Unknown = GameStatus(s='', reply='')


class QuarterStatus(Status):
    """ Quarterly Activity Status """

    @classmethod
    def from_str(cls, s):
        s_ = str(s)
        if s_.lower() == 'full':
            return Full
        if s_.lower() == 'half':
            return Half
        return Inactive

    def active(self):
        """ Boolean indication of activity for the current quarter """
        return self.s.lower() in ('full', 'half')


Full = QuarterStatus(s='FULL', reply='Got it.')
Half = QuarterStatus(s='HALF', reply='Got that too.')
Inactive = QuarterStatus(s='OUT', reply='Got that too.')


class PlayerStatus:
    """ PlayerStatus
    Generally represents a `row` in the back-end, including:
    * Player id info (name, contact, etc)
    * Status for key ongoing events (current game, current quarter) """

    @classmethod
    def from_dict(cls, d):
        """ Create a new PlayerStatus from dict `d` with appropriate keys. """
        id_ = Id(d['ID'])
        phone = Phone(d['Phone'])
        game = GameStatus.from_str(d['game'])
        qtr = QuarterStatus.from_str(d['qtr'])
        return PlayerStatus(id_=id_, phone=phone, game_status=game, qtr_status=qtr)

    def __init__(self, *, id_: Id, phone: Phone, game_status: GameStatus, qtr_status: QuarterStatus):
        assert isinstance(id_, Id)
        self.id_ = id_
        assert isinstance(phone, Phone)
        self.phone = phone
        assert isinstance(game_status, GameStatus)
        self.game_status = game_status
        assert isinstance(qtr_status, QuarterStatus)
        self.qtr_status = qtr_status

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'(name={self.id_}, phone={self.phone}, ' \
               f'game_status={self.game_status}, ' \
               f'qtr_status={self.qtr_status}'

    def valid(self):
        """ Check name & phone are valid """
        return self.id_.valid() and self.phone.valid()

    def pollable(self):
        """ "Poll-ability" == valid info, and an active quarter-status. """
        return self.valid() and self.active()

    def active(self):
        """ Quarter-active status.  Delegated to `self.qtr_status`. """
        return self.qtr_status.active()

    def game_status_known(self):
        """ Game-status known.  Delegated to `self.game_status`. """
        return self.game_status.known()

    def valid_phone(self):
        """ Test phone validity. Delegated to `self.phone`. """
        return self.phone.valid()

    def valid_name(self):
        """ Test name (id) validity.  Delegated to `self.id_`. """
        return self.id_.valid()

    @property
    def name(self):
        return self.id_
