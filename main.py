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

# = Google API =

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# = Discord API =

import discord

# = Facebook API =

import requests


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

def send_to_facebook(events: list[dict]) -> Exception | None:

    page_id_1 = BKB_FACEBOOK_PAGE_ID
    facebook_access_token_1 = BKB_FACEBOOK_PAGE_TOKEN 
    
    msg: list[str] = message_generator(events=events)

    post_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1) # Figure out if correct link.
    payload = {
    'message': msg,
    'access_token': facebook_access_token_1
    }
    r = requests.post(post_url, data=payload)
    print(r.text)

    return None

async def send_to_discord(events: list[dict]) -> list[Exception]:
    """
        events er en dictonary med alle relevante envents for den kommende uke[^1]

        [^1] kommende uke er 7 dager etter den dagen hvor programmet hentet eventer.
    """
    
    if "discord_announcment_client" not in globals():
        print("Client has not been inisiated")
        return NameError("func 'send_to_discord': 'discord_announcment_client' does not exist.")
    # lim inn kode for å sende en str til "annonser", pass på formatering og at det er på riktig kanal
    # IKKE RAISE ERROR! Programmet må kjøre kontinuelig heletiden. Heller returner en Error isteded.
    ret_messages = list()
    for event in message_generator(events):
        try:
            await discord_announcment_client.send(event)
        except Exception as err:
            ret_messages.append(err)
    
    return ret_messages



def main():
    pass

def message_generator(events: dict) -> list[str]:
    """
        Generates a string meant to be sendt to end-clients.
        Fokuserer på 3 nøkkelord i root:
            - item["description"] -> str
            - item["start"]       -> dict
            - item["end"]         -> dict
        NOTE:
            Det er mange nøkkelord vi kan bruke... Dette krever lengere undersøkelse etter vi går live.
    """
    messages = list()
    for item in events: # is going to be replaced by a "standard" function so we can have fledxible text generation 
        start = datetime.datetime.fromisoformat(item["start"])
        end   = datetime.datetime.fromisoformat(item["end"])
        top    = "date: {}\nStart: {} -> End: {}".format(start.date(),":".join(str(start.time()).split(":")[:2]),":".join(str(end.time()).split(":")[:2]))
        middel = item["description"]
        end    = ""

        messages.append("--------------".join([top,middel,end]))

    return messages



def create_contact() -> Exception | None:
    """
        Creates the nessesary connections to services.
        services:
            - Google calendar API (håndter et annet sted, se "Get_2w_google_api()" )
            - Facebook Graph API (muligens trenger ikke?)
            - Discord API
    """
    global discord_announcment_client, facebook_client

    discord_announcment_client = discord.Client().get_guild(BKB_SERVER_ID).get_channel(BKB_ANNOUNCMENT_CHANNEL_ID)
    facebook_client = ""

    return None

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
