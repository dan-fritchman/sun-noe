"""
Messaging, including creation and calls to our Twilio client
Plus a few uses thereof.
"""
import os
import time

from twilio.rest import Client

# Environment setup
account_sid = os.environ['TWILIO_ACCT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
acct_num = os.environ['TWILIO_PHONE_NUM']
app_url = os.environ['APP_URL']

# SMS Client
client = Client(account_sid, auth_token)
DEFAULT_MSG = 'SUNDAY BBALL: '


def send_msg(phone, body):
    """ Send a single SMS message, using our client """
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


def get_polling_method(meth_name=None):
    """ Grab a polling-method by string-key
    Eventually these could be auto-registered somehow;
    for now we just keep a look-up dict of them. """

    methods = dict(
        poll_game_unknowns=poll_game_unknowns,
        poll_dan=poll_dan,
    )

    default_method = poll_game_unknowns
    if meth_name is None:
        return default_method

    # Note missing-entries, other than `None`, will generate KeyErrors
    # This is on the caller to handle.
    return methods[meth_name]


def poll_game_unknowns(msg=DEFAULT_MSG):
    """ Poll everyone with unknown-status for upcoming game """
    print(f'Running poll_game_unknowns with msg={msg}')
    from .sheet import GoogleDocBackend

    be = GoogleDocBackend()
    unknowns = be.get_game_uknowns()
    # FIXME: would be nice to have a "real" way to test mock-up data.
    # unknowns = [('dan', os.environ['DAN_PHONE_NUM')]

    print(f'Unknowns: {str(unknowns)}')
    for u in unknowns:
        print(f'poll_game_unknowns Polling : {u.name}, {u.phone}')
        all_status_msg(name=u.name, phone=u.phone, msg=msg)


def poll_dan(msg=DEFAULT_MSG):
    """Debug method to ping just user `dan` """
    print('Polling Dan')
    all_status_msg(name='dan', phone=os.environ['DAN_PHONE_NUM'], msg=msg)
