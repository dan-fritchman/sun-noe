"""
Polling Script
"""

def main():
    from app.msg import get_unknowns
    [print(p) for p in get_unknowns()]

    from app.msg import poll_dan, poll_unknowns_sunday
    # poll_dan(msg='???')
    # poll_unknowns_sunday()


if __name__ == '__main__':
    main()
