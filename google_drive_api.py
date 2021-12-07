from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from slack_api import send_to_slack

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']


def connect():
    '''Connects the Google Drive API and returns the service.'''
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

    service = build('drive', 'v3', credentials=creds)
    return service


def send_xlsx(service):
    '''Sends a dataset file to Google Drive.'''

    # Call the Drive v3 API
    file_metadata = {'name': 'dataset.xlsx'}
    media = MediaFileUpload(
        'dataset.xlsx', mimetype='application/vnd.ms-excel')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print('File sent to Drive, ID: %s' % file.get('id'))
    send_to_slack('File sent to Drive, ID: %s' % file.get('id'))


def create_folder(service):
    '''Creates a folder in Google Drive.'''
    file_metadata = {
        'name': 'Spreadsheets',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                  fields='id').execute()
    folder_id = file.get('id')
    print('Folder created, ID: %s' % folder_id)
    send_to_slack('Folder created, ID: %s' % folder_id)
    return folder_id


def create_spreadsheet_in_folder(service, folder_id):
    '''Creates spreadsheet in determinated folder.'''
    file_metadata = {
        'name': 'dataset',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [folder_id]
    }
    media = MediaFileUpload('dataset.xlsx',
                            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    spreadsheet_id = file.get('id')
    print('Spreadsheet dataset created inside Spreadsheets folder, ID: %s' %
          spreadsheet_id)
    send_to_slack('Spreadsheet dataset created inside Spreadsheets folder, ID: %s' %
          spreadsheet_id)
    return spreadsheet_id


def google_drive_api():
    try:
        service = connect()
        send_xlsx(service=service)
        folder_id = create_folder(service=service)
        spreadsheet_id = create_spreadsheet_in_folder(
            service=service, folder_id=folder_id)
        return spreadsheet_id, folder_id, service

    except Exception as err:
        print(f'Error occurred: {err}')
