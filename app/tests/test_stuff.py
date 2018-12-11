import pytest


@pytest.fixture(scope='module')
def g():
    from ..sheet import GoogleDocBackend
    g = GoogleDocBackend()
    return g


def test_back_end_connection(g):
    """ Test we can make a back-end connection. """
    p = g.get_players()
    assert len(p)


def test_unknowns(g):
    """ Test we can make a back-end connection. """
    p = g.get_game_unknowns()
    assert isinstance(p, list)


def test_valid(g):
    """ Test we can make a back-end connection. """
    players = g.get_players()
    p = [_ for _ in players if _.valid_phone()]
    assert isinstance(p, list)
    p = [_ for _ in players if not _.valid_phone()]
    assert isinstance(p, list)
    p = [_ for _ in players if _.valid_name()]
    assert isinstance(p, list)
    p = [_ for _ in players if not _.valid_name()]
    assert isinstance(p, list)


def test_debug_df(g):
    """ Check all of our debug, pollable, etc info """
    df = g.debug_df
    assert df is not None
    print(df)
