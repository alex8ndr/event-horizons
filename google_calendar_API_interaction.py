from __future__ import print_function
import icalendar
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    # read ics file
    with open('events.ics', 'rb') as f:
        ical = icalendar.Calendar.from_ical(f.read())


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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        events_calendar = 'f4564373b1300bfc7bbdad03a12c2b7a442c1c5dbc31954dc8d819ef1340f775@group.calendar.google.com'
        #build calendar api service with SCOPES
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        event = None
        for component in ical.walk():
            if component.name == "VEVENT":
                event = {
            'summary': component.get('summary'),
            'location': component.get('location'),
            'start': {
                'dateTime': component.get('dtstart').dt.isoformat(),
                'timeZone': 'America/Toronto'
            },
            'end': {
                'dateTime': component.get('dtend').dt.isoformat(),
                'timeZone': 'America/Toronto'
            }
        }
                event = service.events().insert(calendarId='f4564373b1300bfc7bbdad03a12c2b7a442c1c5dbc31954dc8d819ef1340f775@group.calendar.google.com', body=event).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()