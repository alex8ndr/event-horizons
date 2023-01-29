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
    with open('public/ical/ecsess-electrical-computer-and-software-engineering-student-society.ics', 'r', encoding = "ISO-8859-1") as file:
        ical = icalendar.Calendar.from_ical(file.read())
    cal_dict = {
    'asus': 'f43c8cdeca5ebf46eaac369c33a6132fbd34dac309c4102b4391ebc861754fac@group.calendar.google.com',
    'aus': '5357e8f7749438e036cf0b600e3ca3dbedf3750d04dbc285c6f10498c0eff845@group.calendar.google.com',
    'csus': 'de65a450b2fcf1a9fac4ded53068f89637c3462fbcbd6c84e3cc4ce25a4b1c42@group.calendar.google.com',
    'ecsess': '48e53a709b3a71179ec5d8b56bb29aedbab11589f3f28e037974061e8ebf2120@group.calendar.google.com',
    'mame': 'c7c7eda1340eaaef2f0bffa9b53ed4fb33010324be427d70f34ef98bfa3e10da@group.calendar.google.com',
    'mcgill': 'f4564373b1300bfc7bbdad03a12c2b7a442c1c5dbc31954dc8d819ef1340f775@group.calendar.google.com',
    'sus': '84768e31ba42ab1bae4125a15b4d53c07b87e9ad0784fa4ec2ff9948848b854e@group.calendar.google.com'
    }
    #get all ics file names into a list in the public folder
    ics_files = os.listdir('public/ical')
    ics_files.remove('all.ics')
    




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
        
        #build calendar api service with SCOPES
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        event = None
        calendar_id = None
        for file in ics_files:
            if 'aus' in file:
                calendar_id = cal_dict['aus']
            elif 'asus' in file:
                calendar_id = cal_dict['asus']
            elif 'csus' in file:
                calendar_id = cal_dict['csus']
            elif 'ecsess' in file:
                calendar_id = cal_dict['ecsess']
            elif 'mame' in file:
                calendar_id = cal_dict['mame']
            elif 'mcgill' in file:
                calendar_id = cal_dict['mcgill']
            elif 'sus' in file and not 'asus' in file and not 'csus' in file:
                calendar_id = cal_dict['sus']
            
            with open('public/ical/' + file, 'r', encoding = "ISO-8859-1") as file:
                ical = icalendar.Calendar.from_ical(file.read())
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
                    'dateTime': component.get('dtstart').dt.isoformat(),
                    'timeZone': 'America/Toronto'
                }
            }
                    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()