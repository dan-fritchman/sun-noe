"""
Messaging, including creation and calls to our Twilio client
Plus a few uses thereof.
"""
import os
import time

from twilio.rest import Client

from .sheet import GoogleDocBackend

# Environment setup
account_sid = os.environ['TWILIO_ACCT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
acct_num = os.environ['TWILIO_PHONE_NUM']
app_url = os.environ['APP_URL']

# SMS Client
client = Client(account_sid, auth_token)
DEFAULT_MSG = 'SUNDAY BBALL: '


def send_msg(phone, body):
    print(f'Sending {body} to {phone}')
    return client.api.account.messages.create(to='+1' + phone, from_=acct_num, body=body)


def send_status_msg(name, phone, status):
    """ Send a single link """
    body = f"{app_url}/{name}/{status}"
    send_msg(phone=phone, body=body)


def all_status_msg(name, phone, msg=DEFAULT_MSG):
    """ Send a full set of status links """
    print(f'Requesting status for {name}')

    send_msg(phone=phone, body=msg)
    time.sleep(1.0)

    send_msg(phone=phone, body=os.environ['DOC_EDIT_URL'])
    time.sleep(1.0)

    for status in 'in out tbd'.split():
        send_status_msg(name=name, phone=phone, status=status)
        time.sleep(1.0)


def get_unknowns():
    """ Get a list of active Players with unknown status for the upcoming game. """
    players = GoogleDocBackend().get_players()
    unknowns = []

    for p in players:
        if p.pollable() and not p.game_status_known():
            unknowns.append(p)

    return unknowns


"""
Maybe break this stuff out to a separate polling-module. 
"""


def poll_unknowns_sunday(msg=DEFAULT_MSG):
    """ Poll everyone with unknown-status for upcoming game """
    print(f'Running poll_unknowns_sunday with msg={msg}')

    # Unknowns come back in a list of (name, phone) tuples, at least for now
    unknowns = get_unknowns()
    # FIXME: would be nice to have a "real" way to test mock-up data.
    # unknowns = [('dan', os.environ['DAN_PHONE_NUM')]

    print(f'Unknowns: {str(unknowns)}')
    for u in unknowns:
        print(f'poll_unknowns_sunday Polling : {name}, {ph}')
        all_status_msg(name=u.name, phone=u.phone, msg=msg)


def poll_dan(msg=DEFAULT_MSG):
    """Debug method to ping just user `dan` """
    print('Polling Dan')
    all_status_msg(name='dan', phone=os.environ['DAN_PHONE_NUM'], msg=msg)
