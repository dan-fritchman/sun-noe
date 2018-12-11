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

    def valid(self) -> bool:
        """ Test phone validity.  *Only* accepts ten-digit strings (no punctuation). """
        phone = self.s
        if not isinstance(phone, str):
            return False
        elif len(phone) != 10:
            return False
        else:
            for c in phone:
                if not c.isdigit():
                    return False
            return True


class GameStatus(Cell):
    pass


class QuarterStatus(Cell):
    pass


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
        game = GameStatus(d['game'])
        qtr = GameStatus(d['qtr'])
        return PlayerStatus(id_=id_, phone=phone, game_status=game, qtr_status=qtr)

    def __init__(self, *, id_: Id, phone: Phone, game_status: str, qtr_status: str):
        assert isinstance(id_, Id)
        self.id_ = id_
        assert isinstance(phone, Phone)
        self.phone = phone
        self.game_status = str(game_status).strip()
        self.qtr_status = str(qtr_status).strip()

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'(name={self.id_}, phone={self.phone}, ' \
               f'game_status={self.game_status}, ' \
               f'qtr_status={self.qtr_status}'

    def valid(self):
        """ Check name & phone are valid """
        return self.id_.valid() and self.phone.valid()

    def pollable(self):
        """ Know how to check for validity and "poll-ability" """
        return self.valid() and self.active()

    def active(self):
        """ Boolean indication of activity for the current quarter """
        # FIXME: some kind of status method
        return self.qtr_status.lower() in ('full', 'half')

    def game_status_known(self):
        # FIXME: should be a more central idea of known/ unknown
        return self.game_status.lower() in 'in yes no out '.split()

    def valid_phone(self):
        """ Test phone validity. Delegated to `self.phone`. """
        return self.phone.valid()

    def valid_name(self):
        """ Test name (id) validity.  Delegated to `self.id_`. """
        return self.id_.valid()

    @property
    def name(self):
        return self.id_
