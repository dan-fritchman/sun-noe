import os
from twilio.rest import Client
from sheet import GoogleDocBackend

# Environment setup
account_sid = os.environ['TWILIO_ACCT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
acct_num = os.environ['TWILIO_PHONE_NUM']
app_url = os.environ['APP_URL']

# SMS Client
client = Client(account_sid, auth_token)


def send_msg(phone, body):
    print(f'Sending {body} to {phone}')
    return client.api.account.messages.create(to='+1' + phone, from_=acct_num, body=body)


def send_status_msg(name, phone, status):
    # Send a single link
    body = f"{app_url}/{name}/{status}"
    send_msg(phone=phone, body=body)


def all_status_msg(name, phone):
    # Send a full set of status links

    print(f'Requesting status for {name}')
    send_msg(phone=phone, body='SUNDAY BBALL: ')

    for sts in 'in out tbd'.split():
        send_status_msg(name=name, phone=phone, status=sts)


def valid_phone(phone):
    if not isinstance(phone, str):
        return False
    elif len(phone) != 10:
        return False
    else:
        for c in phone:
            if not c.isdigit():
                return False
        return True


def valid_name(name):
    return isinstance(name, str) and len(name) > 1


def poll_everyone():
    back_end = GoogleDocBackend()
    ids = back_end.col_values('ID')
    phone_nums = back_end.col_values('Phone')

    for name, ph in zip(ids, phone_nums):
        if valid_name(name) and valid_phone(ph):
            print(f'Valid : {name}, {ph}')
            all_status_msg(name=name, phone=ph)
        else:
            print(f'Invalid : {name}, {ph}')


def poll_dan():
    # Debug method to ping just me
    all_status_msg(name='dan', phone=os.environ['DAN_PHONE_NUM'])


def main():
    poll_dan()


if __name__ == '__main__':
    main()
