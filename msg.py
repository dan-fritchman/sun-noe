from twilio.rest import Client

from sheet import GoogleDocBackend

back_end = GoogleDocBackend()

# Find these values at https://twilio.com/user/account
account_sid = "AC43f40d29f4ceebfdd80677e1507f1c91"
auth_token = "b19b822a7a6bfd61088e9632833e0573"
acct_num = "+12674777207"
client = Client(account_sid, auth_token)


def send_status_msg(id, phone, status):
    print(id)
    print(phone)
    print(status)
    """
    message = client.api.account.messages.create(to=f"+1{phone}",
                                                 from_=acct_num,
                                                 body=f"https://desolate-lake-68016.herokuapp.com/{id}/{status}")
    """


def all_status_msg(id, phone):
    # Send a full set of status links
    for sts in 'tbd out in'.split():
        send_status_msg(id=id, phone=phone, status=sts)


ids = back_end.col_values('ID')
phone_nums = back_end.col_values('Phone')

print(ids)
print(phone_nums)

def main():
    pass


if __name__ == '__main__':
    main()
