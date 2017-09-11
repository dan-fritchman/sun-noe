import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Load up the sheet
sheet_name = 'Sunday Noe Bball Debug'
sheet = client.open(sheet_name).sheet1

# Load up headers, verify they are as expected
hdr_names = sheet.row_values(1)
hdrs = dict(zip(hdr_names, range(1, len(hdr_names)+1)))
expected_cols = 'Name ID Phone Sunday Quarter '.split()
for x in expected_cols:
    if x not in hdrs:
        raise ValueError

# Grab a few lists of columns
players = sheet.col_values(col=hdrs['Name'])
ids = sheet.col_values(col=hdrs['ID'])
phs = sheet.col_values(col=hdrs['Phone'])

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)