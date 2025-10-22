# tools/notifications.py
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from config.settings import settings

logger = logging.getLogger(__name__)

def send_sms_confirmation(recipient_phone_number: str, full_name: str, start_time_str: str):
    """Sends an SMS confirmation for a booked meeting using Twilio."""

    if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER]):
        logger.error("Twilio credentials or phone number not configured. Cannot send SMS.")
        return False

    # Ensure recipient number is in E.164 format (e.g., +27821234567)
    # Basic check/add prefix if needed - adapt logic based on how numbers are stored/provided
    if not recipient_phone_number.startswith('+'):
         if len(recipient_phone_number) == 10 and recipient_phone_number.startswith('0'):
             # Assuming South African number format '082...' -> '+2782...'
             recipient_phone_number = f"+27{recipient_phone_number[1:]}"
         else:
             logger.warning(f"Recipient phone number {recipient_phone_number} might not be in E.164 format. SMS may fail.")
             # You might choose to raise an error or attempt sending anyway

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    first_name = full_name.split(' ')[0]
    message_body = (
        f"Hi {first_name}, this is Zappies AI confirming your onboarding call for {start_time_str}. "
        f"You'll also receive an email and calendar invite. See you then!"
    )

    try:
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=recipient_phone_number
        )
        logger.info(f"SMS confirmation sent successfully to {recipient_phone_number} (SID: {message.sid})")
        return True
    except TwilioRestException as e:
        logger.error(f"Failed to send SMS confirmation to {recipient_phone_number}: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred sending SMS to {recipient_phone_number}: {e}")
        return False