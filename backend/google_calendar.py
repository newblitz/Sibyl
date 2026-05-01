from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_service():
    creds = None
    # credentials.json is the OAuth file you downloaded from Google Cloud
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)
    service = build('calendar', 'v3', credentials=creds)
    return service


def create_google_meet_event():
    service = get_google_calendar_service()
    event = {
        'summary': 'Counselling Session',
        'description': 'Online counselling appointment.',
        'start': {
            'dateTime': '2025-10-11T18:00:00+05:30',
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': '2025-10-11T18:30:00+05:30',
            'timeZone': 'Asia/Kolkata',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'randomstring1234'
            }
        },
    }

    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    print("Meeting created:", event.get('hangoutLink'))
    return event.get('hangoutLink')