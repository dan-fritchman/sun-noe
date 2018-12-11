"""
Messaging, including creation and calls to our Twilio client.
Plus a few uses thereof.
"""
import time

from . import config


class SmsMessage(object):
    """ Base class for an SMS Message, or a surrogate therefore. """

    def __init__(self, *, to: str, from_: str, body: str):
        self.to = str(to)
        self.from_ = str(from_)
        self.body = str(body)

    def __repr__(self):
        return f'{self.__class__.__name__}(to={self.to}, from={self.from_}, body={self.body})'

    def send(self):
        raise NotImplementedError


class TwilioMessage(SmsMessage):
    """ SMS Message sent via Twilio client """

    def send(self):
        from twilio.rest import Client as TwilioClient
        tc = TwilioClient(config.account_sid, config.auth_token)
        tc.api.account.messages.create(to='+1' + self.to, from_=self.from_, body=self.body)
        return None


class PrintMessage(SmsMessage):
    """ Testing message-type. Instead of actually sending, just print to console. """

    def send(self):
        print(f'Fake-Sending {self}')


# Default use-case. Some day move to config.
MessageClass = TwilioMessage


def send_msg(phone, body):
    """ Send a single SMS message, using our client """
    print(f'Sending {body} to {phone}')
    msg = MessageClass(to=phone, from_=config.acct_num, body=body)
    return msg.send()


def send_status_msg(name, phone, status):
    """ Send a single link """
    body = f"{config.app_url}/{name}/{status}"
    send_msg(phone=phone, body=body)


def all_status_msg(name, phone, msg=config.DEFAULT_MSG):
    """ Send a full set of status links """
    print(f'Requesting status for {name}')

    send_msg(phone=phone, body=msg)
    time.sleep(1.0)
    # send_msg(phone=phone, body=config.gspread_url)
    # time.sleep(1.0)

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


def poll_game_unknowns(msg=config.DEFAULT_MSG):
    """ Poll everyone with unknown-status for upcoming game """
    print(f'Running poll_game_unknowns with msg={msg}')
    from .sheet import GoogleDocBackend

    be = GoogleDocBackend()
    print(be.debug_df)
    unknowns = be.get_game_unknowns()
    # FIXME: would be nice to have a "real" way to test mock-up data.
    # unknowns = [('dan', os.environ['DAN_PHONE_NUM')]

    print(f'Unknowns: {str(unknowns)}')
    for u in unknowns:
        print(f'poll_game_unknowns Polling : {u.name}, {u.phone}')
        all_status_msg(name=u.name, phone=u.phone, msg=msg)


def poll_dan(msg=config.DEFAULT_MSG):
    """Debug method to ping just user `dan` """
    print('Polling Dan')
    all_status_msg(name='dan', phone=config.host_phone_num, msg=msg)
