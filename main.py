from __future__ import print_function

# Important variables that are private
from var import *


import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.

def Get_2w_google_api():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./tolken/token.json'):
        creds = Credentials.from_authorized_user_file('./tolken/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './tolken/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./tolken/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now_datetime = datetime.datetime.utcnow()
        now = now_datetime.isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Upcoming events for the next 2 weeks')
        events_result = service.events().list(calendarId= BKB_CAL_ID , timeMin=now,
                                              timeMax= (now_datetime + datetime.timedelta(weeks=2)).isoformat() + 'Z', singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        return events

    except HttpError as error:
        print('An error occurred: %s' % error)
        return None

def main():
    pass

if __name__ == "__main__":
    main()
