def test_back_end_connection():
    """ Test we can make a back-end connection. """
    from ..sheet import GoogleDocBackend
    g = GoogleDocBackend()
    p = g.get_players()
    assert len(p)
