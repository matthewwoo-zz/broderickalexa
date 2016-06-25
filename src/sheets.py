from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from flask import json
from oauth2client import client
from oauth2client import tools
from datetime import datetime
import src.constants as constants

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# SCOPES = constants.SCOPES
# CLIENT_SECRET_FILE = constants.CLIENT_SECRET_FILE
# APPLICATION_NAME = constants.APPLICATION_NAME
# spreadsheetId = constants.SPREADSHEET_ID

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Broderick Test'
spreadsheetId = '1Wmt5qXKHMpnpVT7NS6-ZmfxNf4opRz6b3CKl2dRXZU8'



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    rangeName = 'Class Data!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

def create_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    return service

def num_row(service,rangeName):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    row_num = values.__len__()
    if not values:
        print('No data found.')
    return row_num

def tally_all():
    pass

def tally(name):
    service = create_service()
    rangeName = 'Owed!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    for row in values:
        if row[0] == name:
            return row[1]
        return 0

def record(date=datetime.now(), name="Perret", description="Mess in kitchen"):
    service = create_service()
    oldRange = '{}!A1:E'.format(name)
    row_num = num_row(service, oldRange) + 1

    rangeName = '{}!A{}:E'.format(name,row_num)
    valueInputOption = "RAW"
    date = date.strftime('%Y-%m-%d')
    data = {'values':[[date, name, description]]}

    write = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range=rangeName, body=data, valueInputOption=valueInputOption).execute()

    write.update()


