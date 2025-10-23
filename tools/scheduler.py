# tools/scheduler.py
import logging
import datetime
import pytz
from supabase.client import Client, create_client
from config.settings import settings
from tools.notifications import send_sms_reminder
from dateutil.parser import parse

logger = logging.getLogger(__name__)
SAST_TZ = pytz.timezone(settings.VOICE_AGENT_CONFIG.TIMEZONE)

def send_meeting_reminders():
    """
    Scheduled job to find and send reminders for upcoming meetings.
    This function will be run on an interval (e.g., every 30 minutes).
    """
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        now_sast = datetime.datetime.now(SAST_TZ)
        
        logger.info("Scheduler: Running send_meeting_reminders job...")

        # 1. --- 24-Hour Reminders ---
        # Find meetings between 24 and 25 hours from now
        twenty_four_hours_from_now = now_sast + datetime.timedelta(hours=24)
        twenty_five_hours_from_now = now_sast + datetime.timedelta(hours=25)

        resp_24h = supabase.table("meetings").select("*").eq("status", "confirmed").eq("reminder_24h_sent", False).gte("start_time", twenty_four_hours_from_now.isoformat()).lt("start_time", twenty_five_hours_from_now.isoformat()).execute()

        for meeting in resp_24h.data:
            if meeting.get("client_number"):
                logger.info(f"Scheduler: Sending 24h reminder for meeting ID {meeting['id']}")
                start_time_dt = parse(meeting['start_time']).astimezone(SAST_TZ)
                time_str = start_time_dt.strftime('%I:%M %p').replace(' 0', ' ')
                
                success = send_sms_reminder(
                    recipient_phone_number=meeting["client_number"],
                    full_name=meeting["full_name"],
                    start_time_str=time_str,
                    reminder_type="24h"
                )
                if success:
                    supabase.table("meetings").update({"reminder_24h_sent": True}).eq("id", meeting["id"]).execute()
            else:
                # Mark as "sent" to avoid re-checking
                supabase.table("meetings").update({"reminder_24h_sent": True}).eq("id", meeting["id"]).execute()


        # 2. --- Morning-Of Reminders ---
        # Find meetings today, where it's currently 8-9 AM
        if 8 <= now_sast.hour < 9:
            start_of_day = now_sast.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = now_sast.replace(hour=23, minute=59, second=59, microsecond=0)

            resp_morning = supabase.table("meetings").select("*").eq("status", "confirmed").eq("reminder_morning_sent", False).gte("start_time", start_of_day.isoformat()).lte("start_time", end_of_day.isoformat()).execute()

            for meeting in resp_morning.data:
                if meeting.get("client_number"):
                    logger.info(f"Scheduler: Sending morning-of reminder for meeting ID {meeting['id']}")
                    start_time_dt = parse(meeting['start_time']).astimezone(SAST_TZ)
                    time_str = start_time_dt.strftime('%I:%M %p').replace(' 0', ' ')
                    
                    success = send_sms_reminder(
                        recipient_phone_number=meeting["client_number"],
                        full_name=meeting["full_name"],
                        start_time_str=time_str,
                        reminder_type="morning"
                    )
                    if success:
                        supabase.table("meetings").update({"reminder_morning_sent": True}).eq("id", meeting["id"]).execute()
                else:
                    supabase.table("meetings").update({"reminder_morning_sent": True}).eq("id", meeting["id"]).execute()

        
        # 3. --- 1-Hour Reminders ---
        # Find meetings between 60 and 90 minutes from now (to run on a 30-min job interval)
        one_hour_from_now = now_sast + datetime.timedelta(hours=1)
        ninety_min_from_now = now_sast + datetime.timedelta(minutes=90)
        
        resp_1h = supabase.table("meetings").select("*").eq("status", "confirmed").eq("reminder_1h_sent", False).gte("start_time", one_hour_from_now.isoformat()).lt("start_time", ninety_min_from_now.isoformat()).execute()

        for meeting in resp_1h.data:
            if meeting.get("client_number"):
                logger.info(f"Scheduler: Sending 1h reminder for meeting ID {meeting['id']}")
                start_time_dt = parse(meeting['start_time']).astimezone(SAST_TZ)
                time_str = start_time_dt.strftime('%I:%M %p').replace(' 0', ' ')

                success = send_sms_reminder(
                    recipient_phone_number=meeting["client_number"],
                    full_name=meeting["full_name"],
                    start_time_str=time_str,
                    reminder_type="1h"
                )
                if success:
                    supabase.table("meetings").update({"reminder_1h_sent": True}).eq("id", meeting["id"]).execute()
            else:
                supabase.table("meetings").update({"reminder_1h_sent": True}).eq("id", meeting["id"]).execute()
        
        logger.info("Scheduler: Reminder job finished.")

    except Exception as e:
        logger.error(f"Error in scheduled reminder job: {e}", exc_info=True)