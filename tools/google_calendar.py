# tools/google_calendar.py
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient import errors
from config.settings import settings
import pytz
from dateutil.parser import parse

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = settings.SERVICE_ACCOUNT_FILE
CALENDAR_ID = settings.GOOGLE_CALENDAR_ID

def get_calendar_service():
    """Returns an authenticated Google Calendar service object."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_available_slots(date: str) -> list[str]:
    service = get_calendar_service()
    sast_tz = pytz.timezone("Africa/Johannesburg")
    day_start = sast_tz.localize(datetime.datetime.fromisoformat(date))
    day_end = day_start + datetime.timedelta(days=1)
    events_result = service.events().list(
        calendarId=CALENDAR_ID, timeMin=day_start.isoformat(),
        timeMax=day_end.isoformat(), singleEvents=True, orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    working_hours_start = day_start.replace(hour=9, minute=0, second=0, microsecond=0)
    working_hours_end = day_start.replace(hour=17, minute=0, second=0, microsecond=0)
    available_slots = []
    current_time = working_hours_start
    while current_time < working_hours_end:
        slot_end = current_time + datetime.timedelta(minutes=60)
        is_free = True
        for event in events:
            event_start = parse(event['start'].get('dateTime')).astimezone(sast_tz)
            event_end = parse(event['end'].get('dateTime')).astimezone(sast_tz)
            if not (slot_end <= event_start or current_time >= event_end):
                is_free = False
                break
        if is_free:
            available_slots.append(current_time.isoformat())
        current_time += datetime.timedelta(minutes=60)
    return available_slots


# --- THIS FUNCTION IS UPDATED ---
def find_event_by_details(email: str, original_start_time: str) -> str | None:
    """Finds a Google Calendar event ID using a reliable private property search."""
    service = get_calendar_service()
    sast_tz = pytz.timezone("Africa/Johannesburg")
    start_time = parse(original_start_time)
    if start_time.tzinfo is None:
        start_time = sast_tz.localize(start_time)
        
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time.isoformat(),
        timeMax=(start_time + datetime.timedelta(minutes=1)).isoformat(),
        # Use the more reliable private property search instead of 'q'
        privateExtendedProperty=f"lead_email={email}",
        singleEvents=True
    ).execute()
    events = events_result.get('items', [])
    return events[0]['id'] if events else None

# ... (update_calendar_event and delete_calendar_event remain the same) ...
def update_calendar_event(event_id: str, new_start_time: str) -> dict:
    service = get_calendar_service()
    sast_tz = pytz.timezone("Africa/Johannesburg")
    start = parse(new_start_time)
    if start.tzinfo is None:
        start = sast_tz.localize(start)
    end = start + datetime.timedelta(minutes=60)
    event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()
    event['start']['dateTime'] = start.isoformat()
    event['end']['dateTime'] = end.isoformat()
    updated_event = service.events().update(
        calendarId=CALENDAR_ID, eventId=event_id, body=event
    ).execute()
    return updated_event

def delete_calendar_event(event_id: str) -> None:
    service = get_calendar_service()
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
    except errors.HttpError as e:
        if e.resp.status == 410:
            print(f"Event {event_id} was already gone.")
        else:
            raise

# --- THIS FUNCTION IS UPDATED ---
def create_calendar_event(start_time: str, summary: str, description: str, attendees: list[str]) -> dict:
    """Creates a new event with an explicit timezone."""
    service = get_calendar_service()
    sast_tz = pytz.timezone("Africa/Johannesburg")

    # --- THIS IS THE FIX ---
    # Parse the incoming time string
    parsed_start_time = parse(start_time)

    # Check if the datetime object is already timezone-aware
    if parsed_start_time.tzinfo is not None:
        # If it is, convert it to the correct local timezone (SAST)
        start = parsed_start_time.astimezone(sast_tz)
    else:
        # If it's naive, localize it as before
        start = sast_tz.localize(parsed_start_time)

    now_sast = datetime.datetime.now(sast_tz)
    if start < now_sast:
        raise ValueError("Cannot book an appointment in the past.")
    if start.date() == now_sast.date():
        raise ValueError("Cannot book a same-day appointment. Please book for the next business day or later.")
    
    start -= datetime.timedelta(minutes=120)
    end = start + datetime.timedelta(minutes=60)

    full_description = description
    lead_email = attendees[0] if attendees else 'N/A'
    if lead_email != 'N/A':
        full_description += f"\n\n---\nLead Contact: {lead_email}"

    event = {
        'summary': summary, 
        'description': full_description,
        'start': {'dateTime': start.isoformat(), 'timeZone': 'Africa/Johannesburg'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Africa/Johannesburg'},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 24 * 60}, {'method': 'popup', 'minutes': 10}]},
        'extendedProperties': {
            'private': {
                'lead_email': lead_email
            }
        }
    }
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event