from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from . import config


def get_upcoming_conferences(N=10):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    service = build('calendar', 'v3', credentials=config.creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # calender_id = 'primary'
    calender_id = 'simula.no_4squutglt7es60hu3c212kijgk@group.calendar.google.com'
    msg = ['Getting the upcoming 10 events from the Comphy Conference calendar']
    events_result = service.events().list(calendarId=calender_id, timeMin=now,
                                        maxResults=N, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        msg.append('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        msg.append(f"{start}: {event['summary']}")


    return '\n'.join(msg)
