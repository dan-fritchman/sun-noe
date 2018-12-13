""" App Configuration """

import os

# Environment setup
account_sid = os.environ['TWILIO_ACCT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
acct_num = os.environ['TWILIO_PHONE_NUM']
app_url = os.environ['APP_URL']
host_phone_num = os.environ['DAN_PHONE_NUM']
gspread_url = os.environ['DOC_EDIT_URL']
gspread_json = os.environ['GSPREAD_JSON']
polling_key = os.environ['POLLING_KEY']

# Default behaviors
DEFAULT_MSG = 'SUNDAY BBALL: '


def get_message_class():
    """ Configuration of which message-class to use. """
    from .msg import PrintMessage, TwilioMessage
    return TwilioMessage
