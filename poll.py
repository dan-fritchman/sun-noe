""" Local Polling Script """


def main():
    from app.sheet import GoogleDocBackend
    back_end = GoogleDocBackend()
    [print(p) for p in back_end.get_game_uknowns()]

    from app.msg import poll_dan, poll_game_unknowns
    poll_dan(msg='???')
    # poll_game_unknowns()


if __name__ == '__main__':
    main()
