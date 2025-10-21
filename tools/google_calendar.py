# tools/google_calendar.py
import datetime
import json
import base64
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient import errors
from config.settings import settings
import pytz
from dateutil.parser import parse

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = settings.GOOGLE_CALENDAR_ID
# Use the centralized timezone from settings
SAST_TZ = pytz.timezone(settings.VOICE_AGENT_CONFIG.TIMEZONE)

logger = logging.getLogger(__name__)

def get_calendar_service():
    """
    Returns an authenticated Google Calendar service object.
    It now uses the GOOGLE_CREDENTIALS_STR from settings, which is
    more robust for cloud deployment.
    """
    creds_str = settings.GOOGLE_CREDENTIALS_STR
    if not creds_str:
        logger.error("GOOGLE_CREDENTIALS_JSON environment variable not set.")
        raise ValueError("Google Credentials are not configured on the server.")
    
    try:
        if creds_str.startswith('{'):
            creds_info = json.loads(creds_str)
        else:
            decoded_creds = base64.b64decode(creds_str).decode('utf-8')
            creds_info = json.loads(decoded_creds)
            
        creds = service_account.Credentials.from_service_account_info(
            creds_info, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        return service
        
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.error(f"Failed to decode or load GOOGLE_CREDENTIALS_JSON: {e}")
        raise ValueError(f"Failed to load Google credentials. Error: {e}")

def get_available_slots(date: str) -> list[str]:
    """
    Checks for available slots on a specific date, now using
    centralized business logic from settings.
    """
    service = get_calendar_service()
    try:
        # Localize the start of the day
        day_start = SAST_TZ.localize(datetime.datetime.fromisoformat(date))
    except ValueError:
        logger.warning(f"Invalid date format received for get_available_slots: {date}")
        return []
        
    day_end = day_start + datetime.timedelta(days=1)
    
    # Use business hour settings
    working_hours_start = day_start.replace(
        hour=settings.VOICE_AGENT_CONFIG.BUSINESS_HOURS_START, 
        minute=0, second=0, microsecond=0
    )
    working_hours_end = day_start.replace(
        hour=settings.VOICE_AGENT_CONFIG.BUSINESS_HOURS_END, 
        minute=0, second=0, microsecond=0
    )
    
    # Fetch events for the entire day to check against
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID, 
            timeMin=day_start.isoformat(),
            timeMax=day_end.isoformat(), 
            singleEvents=True, 
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
    except Exception as e:
        logger.error(f"Error fetching calendar events: {e}")
        return [] # Return empty list on error

    available_slots = []
    current_time = working_hours_start
    slot_duration = datetime.timedelta(minutes=settings.VOICE_AGENT_CONFIG.APPOINTMENT_DURATION_MINUTES)

    while current_time < working_hours_end:
        slot_end = current_time + slot_duration
        
        # Ensure the slot *ends* within working hours
        if slot_end > working_hours_end:
            break
            
        is_free = True
        for event in events:
            event_start = parse(event['start'].get('dateTime')).astimezone(SAST_TZ)
            event_end = parse(event['end'].get('dateTime')).astimezone(SAST_TZ)
            
            # Check for overlap:
            # (Slot starts < Event ends) and (Slot ends > Event starts)
            if (current_time < event_end and slot_end > event_start):
                is_free = False
                break
                
        if is_free:
            available_slots.append(current_time.isoformat())
            
        # Move to the next slot (can be customized, e.g., 30-min increments)
        current_time += datetime.timedelta(minutes=60) 
        
    return available_slots


def find_event_by_details(email: str, original_start_time: str) -> str | None:
    """Finds a Google Calendar event ID using a reliable private property search."""
    service = get_calendar_service()
    start_time = parse(original_start_time)
    if start_time.tzinfo is None:
        start_time = SAST_TZ.localize(start_time)
        
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_time.isoformat(),
            timeMax=(start_time + datetime.timedelta(minutes=1)).isoformat(),
            privateExtendedProperty=f"lead_email={email}",
            singleEvents=True
        ).execute()
        events = events_result.get('items', [])
        return events[0]['id'] if events else None
    except Exception as e:
        logger.error(f"Error finding event by details: {e}")
        return None

def update_calendar_event(event_id: str, new_start_time: str) -> dict:
    """Updates an existing calendar event's time."""
    service = get_calendar_service()
    start = parse(new_start_time)
    if start.tzinfo is None:
        start = SAST_TZ.localize(start)
    
    end = start + datetime.timedelta(minutes=settings.VOICE_AGENT_CONFIG.APPOINTMENT_DURATION_MINUTES)
    
    event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()
    event['start']['dateTime'] = start.isoformat()
    event['end']['dateTime'] = end.isoformat()
    
    updated_event = service.events().update(
        calendarId=CALENDAR_ID, eventId=event_id, body=event
    ).execute()
    return updated_event

def delete_calendar_event(event_id: str) -> None:
    """Deletes a calendar event."""
    service = get_calendar_service()
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
    except errors.HttpError as e:
        if e.resp.status == 410:
            logger.warning(f"Event {event_id} was already deleted.")
        else:
            raise

def create_calendar_event(start_time: str, summary: str, description: str, attendees: list[str]) -> dict:
    """Creates a new event with an explicit timezone."""
    service = get_calendar_service()

    parsed_start_time = parse(start_time)

    if parsed_start_time.tzinfo is not None:
        start = parsed_start_time.astimezone(SAST_TZ)
    else:
        start = SAST_TZ.localize(parsed_start_time)

    now_sast = datetime.datetime.now(SAST_TZ)
    
    # Validation logic
    if start < now_sast:
        raise ValueError("Cannot book an appointment in the past.")
    if start.date() == now_sast.date():
        raise ValueError("Cannot book a same-day appointment. Please book for the next business day or later.")
    
    end = start + datetime.timedelta(minutes=settings.VOICE_AGENT_CONFIG.APPOINTMENT_DURATION_MINUTES)

    full_description = description
    lead_email = attendees[0] if attendees else 'N/A'
    if lead_email != 'N/A':
        full_description += f"\n\n---\nLead Contact: {lead_email}"

    event = {
        'summary': summary,
        'description': full_description,
        'start': {'dateTime': start.isoformat(), 'timeZone': settings.VOICE_AGENT_CONFIG.TIMEZONE},
        'end': {'dateTime': end.isoformat(), 'timeZone': settings.VOICE_AGENT_CONFIG.TIMEZONE},
        # 'attendees': [{'email': email} for email in attendees], # <-- REMOVE or COMMENT OUT
        'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 24 * 60}, {'method': 'popup', 'minutes': 10}]},
        'extendedProperties': {
            'private': {
                'lead_email': lead_email
            }
        }
    }
    # Change sendUpdates to "none" as we aren't inviting attendees via API
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event, sendUpdates="none").execute() # <-- CHANGE sendUpdates
    return created_event