from google_drive_api import google_drive_api
from google_sheets_api import google_sheets_api

if __name__ == '__main__':
    spreadsheet_id = google_drive_api()
    google_sheets_api(spreadsheet_id)
