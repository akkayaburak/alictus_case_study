from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_drive_api import SCOPES

# The range of a sample spreadsheet.


def connect():
    '''Connects the Sheets API and returns the service.'''
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_drive_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    return service


def get_spreadsheet(service, spreadsheet_id):
    '''Gets the determined spreadsheet.'''
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range='A:F').execute()
    values = result.get('values', [])

    if not values:
        raise Exception('No data found.')
    print('Spreadsheet found')
    return values


def create_and_move_spreadsheets(service, values, folder_id, drive_service):
    '''Creates spreadsheet for each campaign and moves them to Spreadsheets folder'''
    spreadsheets = service.spreadsheets()
    for row in values[1:]:
        spreadsheet = {
            'properties': {
                'title': row[0],
            }
        }

        spreadsheet = spreadsheets.create(body=spreadsheet).execute()
        spreadsheet_id = spreadsheet.get('spreadsheetId')
        print('Spreadsheet created for campaign {0},  ID: {1}'.format(
            row[0], spreadsheet_id))

        values = [
            [
                'Campaign name',
                'Total Impression',
                'Total Clicks',
                'CTR (%)',
                'CPC',
                'Total App Install',
                'Total Budget',

            ],
            [
                row[0],
                row[1],
                row[2],
                row[3],
                row[3],
                row[4],
                float(row[2]) * float(row[3])
            ]
        ]
        data = [
            {
                'range': 'A:G',
                'values': values
            },
        ]
        body = {
            'data': data,
            'valueInputOption': 'RAW'
        }

        spreadsheets.values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

        drive_service.files().update(fileId=spreadsheet_id,
                                     addParents=folder_id, removeParents='root').execute()

        print('Spreadsheet moved to Spreadsheets folder for campaign {0},  ID: {1}'.format(
            row[0], spreadsheet_id))


def google_sheets_api(spreadsheet_id, folder_id, drive_service):
    try:
        service = connect()
        spreadsheet = get_spreadsheet(
            service=service, spreadsheet_id=spreadsheet_id)
        create_and_move_spreadsheets(service=service, values=spreadsheet,
                                     folder_id=folder_id, drive_service=drive_service)

    except Exception as err:
        print(f'Error occurred: {err}')
