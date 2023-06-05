import datetime
import json
import logging
import os.path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/spreadsheets']


logging.basicConfig(level=logging.DEBUG)


class CalendarEvent:
    def __init__(self, date: str, desc: str):
        self.date = date
        self.desc = desc

    def __repr__(self):
        return f'{self.date} {self.desc}'

    def __iter__(self):
        return iter([self.date, self.desc])


class CalendarToSheets:
    def __init__(self, task: str = 'Algorithms Brainstorming') -> None:
        self.spreadsheet_id = None
        self.task = task
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def parse_url(self, s: str) -> str:
        look_for = 'href="'
        try:
            href_pos_start = s.index(look_for)
            href_pos_end = s.index('"', href_pos_start + len(look_for))
            return s[href_pos_start + len(look_for): href_pos_end]
        except ValueError:
            return s

    def get_cal_events(self) -> List[CalendarEvent]:
        events = []
        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Call the Calendar API
            res = service.events().list(calendarId='primary', q=self.task).execute().get('items', [])

            if not res:
                logging.error('No events found.')
                return

            for event in res:
                if event.get('status', None) == 'confirmed' and event.get('description', '') != '':
                    events.append(CalendarEvent(
                        date=datetime.datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).strftime('%Y-%m-%d'),
                        desc=self.parse_url(event.get('description', ''))
                    ))

        except HttpError as error:
            logging.exception('An error occurred: %s' % error)
        return events

    def create_sheet(self) -> str:
        persistent_file_name = 'persistent.json'
        if os.path.isfile(persistent_file_name):
            with open(persistent_file_name, 'r') as f:
                obj = json.load(f)
                self.spreadsheet_id = obj['spreadsheet_id']
                logging.info(f'Loaded spreadsheet ID from persistent storage: {self.spreadsheet_id}')
                return self.spreadsheet_id
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            spreadsheet = {
                'properties': {
                    'title': self.task
                }
            }
            spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
            self.spreadsheet_id = spreadsheet.get('spreadsheetId')
            logging.info(f'Spreadsheet ID: {self.spreadsheet_id}')
            with open(persistent_file_name, 'w') as f:
                json.dump(dict(spreadsheet_id=self.spreadsheet_id), f)
            return self.spreadsheet_id
        except HttpError as error:
            logging.exception(f'An error occurred: {error}')
            return error

    def update_events_in_sheet(self, events: List[CalendarEvent]) -> None:
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            values = [
                [
                    # Cell values ...
                ],
                # Additional rows ...
            ]
            body = {
                'values': [[date, desc] for date, desc in events]
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id, range=f'A1:B{len(events)}',
                valueInputOption='USER_ENTERED', body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


if __name__ == '__main__':
    cal2sheets = CalendarToSheets('Algorithms Brainstorming')
    algo_events = cal2sheets.get_cal_events()
    logging.info(algo_events)
    cal2sheets.create_sheet()
    cal2sheets.update_events_in_sheet(algo_events)
