"""
TODO:
    [ ] Interact with API
        [ ] Investigate Facebook API
        [ ] Investigate Discord API
    [ ] create "calendar-to-post" pipeline
"""


from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Important variables that are private
from var import *
# `var` file contains the following variables:
#   BKB_CAL_ID [string] -> Identifying string for a particular calendar 

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

def send_to_facebook(events: dict) -> Exception | None:
    if "facebook_client" not in globals():
        print("Client has not been inisiated")
        return NameError("func 'send_to_facebook': 'facebook_client' does not exist.")

    page_id_1 = 123456789 # wrong id, need to find right one
    facebook_access_token_1 = 'paste-your-page-access-token-here' # wrong token, need to find right one
    
    msg = message_generator(events=events)

    post_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1)
    payload = {
    'message': msg,
    'access_token': facebook_access_token_1
    }
    r = requests.post(post_url, data=payload)
    print(r.text)

def send_to_discord(events: dict) -> Exception | None:
    """
        events er en dictonary med alle relevante envents for den kommende uke[^1]

        [^1] kommende uke er 7 dager etter den dagen hvor programmet hentet eventer.
    """
    
    if "discord_client" not in globals():
        print("Client has not been inisiated")
        return NameError("func 'send_to_discord': 'discord_client' does not exist.")
    # lim inn kode for å sende en str til "annonser", pass på formatering og at det er på riktig kanal
    # IKKE RAISE ERROR! Programmet må kjøre kontinuelig heletiden. Heller returner en Error isteded.
    pass

def main():
    pass

def message_generator(events: dict):
    """
        Generates a string meant to be sendt to end-clients.
    """
    pass



def create_contact() -> Exception | None:
    """
        Creates the nessesary connections to services.
        services:
            - Google calendar API
            - Facebook Graph API (muligens trenger ikke?)
            - Discord API
    """
    global discord_client, facebook_client, google_calendar_client

    discord_client, facebook_client, google_calendar_client = discord.Client(), "", build('calendar', 'v3', credentials=creds)

def time_diff(date1: datetime.datetime, date2: datetime.datetime) -> Exception | datetime.timedelta:
    diff = date2 - date1

    if datetime.timedelta() < diff < datetime.timedelta(hour = 24):
        return diff
    elif diff < datetime.timedelta():
        return datetime.timedelta()
    elif diff > datetime.timedelta(days=1):
        return datetime.timedelta(days=1)
    else:
        return ValueError("The difference is not messurable.")

if __name__ == "__main__":
    create_contact()
    send_to_discord({})
