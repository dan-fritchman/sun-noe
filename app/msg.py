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
    # Send a single link
    body = f"{app_url}/{name}/{status}"
    send_msg(phone=phone, body=body)


def all_status_msg(name, phone, msg=DEFAULT_MSG):
    # Send a full set of status links

    print(f'Requesting status for {name}')
    send_msg(phone=phone, body=msg)
    time.sleep(1.0)

    send_msg(phone=phone, body=os.environ['DOC_EDIT_URL'])
    time.sleep(1.0)

    for status in 'in out tbd'.split():
        send_status_msg(name=name, phone=phone, status=status)
        time.sleep(1.0)


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


def poll_everyone(msg=DEFAULT_MSG):
    back_end = GoogleDocBackend()
    ids = back_end.col_values('ID')
    phone_nums = back_end.col_values('Phone')

    for name, ph in zip(ids, phone_nums):
        if valid_name(name) and valid_phone(ph):
            print(f'Valid : {name}, {ph}')
            all_status_msg(name=name, phone=ph, msg=msg)
        else:
            print(f'Invalid : {name}, {ph}')


def known_status(status):
    return status.lower().strip() in 'in yes no out full half'.split()


def get_unknowns(status_col='Sunday'):
    # Look up players without known status in column <status_col>

    back_end = GoogleDocBackend()

    ids = back_end.col_values('ID')
    phone_nums = back_end.col_values('Phone')
    statuses = back_end.col_values(status_col)
    assert len(ids) == len(phone_nums)
    assert len(statuses) == len(phone_nums)

    unknowns = []

    for _ in range(len(ids)):
        name = ids[_]
        ph = phone_nums[_]
        sts = statuses[_]

        if valid_name(name) and valid_phone(ph):
            print(f'Valid : {name}, {ph}. Status = {sts}')

            if known_status(sts):
                print(f'Confirmed status for {name} - {ph}')
            else:
                print(f'Unknown status for {name} - {ph}')
                unknowns.append((name, ph))
                # print(f'Sending status links to : {name}, {ph}')
                # all_status_msg(name=name, phone=ph, msg=msg)
        else:
            print(f'Invalid : {name}, {ph}')

    return unknowns


def qtr_status_msg(*, name, phone, qname, msg):
    # Send a full set of status links for quarter <qname>

    print(f'Sending quarter-status msg for {name}')
    send_msg(phone=phone, body=msg)
    time.sleep(1.0)

    send_msg(phone=phone, body=os.environ['DOC_EDIT_URL'])
    time.sleep(1.0)

    for status in 'out half full '.split():
        body = f'{app_url}/{name}/quarter/{qname}/{status}'
        send_msg(phone=phone, body=body)
        time.sleep(1.0)


def poll_qtr(players, qname, msg):
    for p in players:
        name = p[0]
        phone = p[1]
        qtr_status_msg(name=name, phone=phone, qname=qname, msg=msg)


def poll_unknowns_sunday(msg=DEFAULT_MSG):
    # Unknowns come back in a list of (name, phone) tuples, at least for now
    msgs = []

    unknowns = get_unknowns(status_col='Sunday')
    msg = f'Unknowns: {str(unknowns)}'
    msgs.append(msg)
    print(msg)

    for u in unknowns:
        name = u[0]
        ph = u[1]

        msg = f'Sending status links to : {name}, {ph}'
        msgs.append(msg)
        print(msg)

        all_status_msg(name=name, phone=ph, msg=msg)

    return msgs


def poll_dan(msg=DEFAULT_MSG):
    """Debug method to ping just user `dan` """
    print('Polling Dan')
    all_status_msg(name='dan', phone=os.environ['DAN_PHONE_NUM'], msg=msg)
    return ['Polled dan']


def main():
    pass


def poll_q2():
    # Poll unknowns for the quarter
    u = get_unknowns(status_col='Q2_2018')
    print(u)

    to_poll = u
    poll_qtr(players=to_poll,
             qname='Q2_2018',
             msg='Sunday BBall Q2 2018: ')


if __name__ == '__main__':
    main()
