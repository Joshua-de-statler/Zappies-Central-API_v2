# tools/email_sender.py
import smtplib
import logging
import html # Added for sanitizing history
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ORIGINAL FUNCTION 1 ---
def send_confirmation_email(recipient_email: str, full_name: str, start_time: str, meeting_id: str):
    """Sends a meeting confirmation email with a confirmation link (for agent flow)."""
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_APP_PASSWORD

    if not sender_email or not sender_password:
        logger.error("Sender email or password not configured. Cannot send confirmation email.")
        return False

    confirmation_url = f"{settings.API_BASE_URL}/confirm-meeting/{meeting_id}"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Please Confirm Your Onboarding Call with Zappies AI"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # --- Using the improved HTML template ---
    html_body = f"""
<!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">

<head>
    <title></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 0; }}
        a[x-apple-data-detectors] {{ color: inherit !important; text-decoration: inherit !important; }}
        #MessageViewBody a {{ color: inherit; text-decoration: none; }}
        p {{ line-height: inherit }}
        .desktop_hide, .desktop_hide table {{ mso-hide: all; display: none; max-height: 0px; overflow: hidden; }}
        .image_block img+div {{ display: none; }}
        @media (max-width:560px) {{
            .row-content {{ width: 100% !important; }}
            .stack .column {{ width: 100%; display: block; }}
            .mobile_hide {{ display: none; }}
            .desktop_hide, .desktop_hide table {{ display: table !important; max-height: none !important; }}
        }}
    </style>
</head>

<body style="background-color: transparent; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
    <table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: transparent;">
        <tbody>
            <tr>
                <td>
                    <table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                       <tr>
                        <td>
                            <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; color: #000000; width: 540px; margin: 0 auto;" width="540">
                                <tbody>
                                    <tr>
                                        <td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top;">
                                            <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                                <tr>
                                                    <td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
                                                        <div class="alignment" align="center">
                                                            <div style="max-width: 81px;"><img src="https://ab8565207c.imgdist.com/pub/bfra/a9yo6qej/hp6/5nn/xlp/favicon.png" style="display: block; height: auto; border: 0; width: 100%;" width="81" alt="Zappies AI Logo" title="Zappies AI Logo"></div>
                                                        </div>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    </tbody></table>
                    <table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                        <tbody>
                            <tr>
                                <td>
                                    <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border: 1px solid #e2e2e2; border-radius: 20px; color: #000000; width: 540px; margin: 0 auto;" width="540">
                                        <tbody>
                                            <tr>
                                                <td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding: 25px 15px 25px 15px; vertical-align: middle;">
                                                    <h2 style="margin: 0; color: #000000; font-family: Arial, Helvetica, sans-serif; font-size: 24px; font-weight: 700; text-align: center; margin-bottom: 15px;">Confirm Your Onboarding Call</h2>
                                                    <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center; margin-bottom: 5px;">Hi {full_name},</p>
                                                    <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center;">Thanks for booking your 'Project Pipeline AI' onboarding call for:</p>
                                                    <p style="margin: 0; color:#5b0202; font-family:Arial, Helvetica, sans-serif; font-size:18px; font-weight: bold; text-align: center; margin-top: 10px; margin-bottom: 15px;">{start_time}</p>
                                                    <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center; margin-bottom: 25px;">To secure your spot, please click the button below to confirm:</p>
                                                    <table class="button_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                                        <tr>
                                                            <td style="text-align:center;">
                                                                <div align="center">
                                                                    <a href="{confirmation_url}" target="_blank" style="text-decoration:none; display:inline-block; color:#fff1dd; background-color:#5b0202; border-radius:4px; width:auto; border:0; padding:10px 25px; font-family:Arial, Helvetica, sans-serif; font-size:18px; text-align:center; mso-border-alt:none; word-break:keep-all;">
                                                                        <span style="word-break: break-word; line-height: 36px;">Confirm Your Meeting</span>
                                                                    </a>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                     <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center; margin-top: 25px;">We're excited to connect with you!</p>
                                                     <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center; margin-top: 10px;">Best,<br>The Zappies AI Team</p>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                        <tbody><tr><td><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; color: #000000; width: 540px; margin: 0 auto;" width="540"><tbody><tr><td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top;"><div class="spacer_block block-1" style="height:60px;line-height:60px;font-size:1px;">&#8202;</div></td></tr></tbody></table></td></tr></tbody>
                    </table>
                </td>
            </tr>
        </tbody>
    </table>
</body>
</html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logger.info(f"Confirmation email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {e}", exc_info=True)
        return False

# --- ORIGINAL FUNCTION 2 ---
def send_handover_email(conversation_id: str, history: list):
    """Sends a human handover notification with the chat history."""
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_APP_PASSWORD
    recipient_email = settings.HANDOVER_EMAIL

    if not all([sender_email, sender_password, recipient_email]):
        logger.error("Email configuration is incomplete. Cannot send handover email.")
        return False

    history_html = ""
    for message in history:
        speaker = "User" if message.type == 'human' else "AI"
        content = html.escape(message.content) # Use html.escape
        history_html += f'<p style="margin: 5px 0;"><strong>{speaker}:</strong> {content}</p>'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Human Handover Requested: Conversation ID {conversation_id}"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    html_body = f"""
    <html>
    <body style="font-family: sans-serif;">
        <h2>Human Handover Request</h2>
        <p>A user has requested to speak with a human agent.</p>
        <p><strong>Conversation ID:</strong> {conversation_id}</p>
        <hr>
        <h3>Conversation History:</h3>
        <div style="background-color: #f4f4f4; border-left: 3px solid #ccc; padding: 10px; max-height: 400px; overflow-y: auto;">
            {history_html}
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logger.info(f"Handover notification sent successfully for conversation {conversation_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send handover email: {e}", exc_info=True)
        return False

# --- NEW FUNCTION ---
def send_direct_booking_confirmation(recipient_email: str, full_name: str, start_time: str):
    """
    Sends a direct meeting confirmation email (no link) for synchronous bookings
    (e.g., from the voice agent). Uses the same HTML template structure.
    """
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_APP_PASSWORD

    if not sender_email or not sender_password:
        logger.error("Sender email or password not configured. Cannot send direct confirmation email.")
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Your Onboarding Call with Zappies AI is Confirmed!"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # --- Using a structure similar to the confirmation email ---
    html_body = f"""
<!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">
 <head>
    <title></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 0; }}
        a[x-apple-data-detectors] {{ color: inherit !important; text-decoration: inherit !important; }}
        #MessageViewBody a {{ color: inherit; text-decoration: none; }}
        p {{ line-height: inherit }}
        .desktop_hide, .desktop_hide table {{ mso-hide: all; display: none; max-height: 0px; overflow: hidden; }}
        .image_block img+div {{ display: none; }}
         @media (max-width:560px) {{
            .row-content {{ width: 100% !important; }}
            .stack .column {{ width: 100%; display: block; }}
            .mobile_hide {{ display: none; }}
            .desktop_hide, .desktop_hide table {{ display: table !important; max-height: none !important; }}
        }}
    </style>
</head>
 <body style="background-color: transparent; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
    <table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: transparent;">
        <tbody>
            <tr>
                <td>
                     <table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                       <tbody><tr><td>
                            <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; color: #000000; width: 540px; margin: 0 auto;" width="540">
                                <tbody><tr><td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top;">
                                    <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                        <tr><td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
                                            <div class="alignment" align="center">
                                                <div style="max-width: 81px;"><img src="https://ab8565207c.imgdist.com/pub/bfra/a9yo6qej/hp6/5nn/xlp/favicon.png" style="display: block; height: auto; border: 0; width: 100%;" width="81" alt="Zappies AI Logo" title="Zappies AI Logo"></div>
                                            </div>
                                        </td></tr>
                                    </table>
                                </td></tr></tbody>
                            </table>
                       </td></tr></tbody>
                    </table>
                    <table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                        <tbody>
                            <tr>
                                <td>
                                    <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border: 1px solid #e2e2e2; border-radius: 20px; color: #000000; width: 540px; margin: 0 auto;" width="540">
                                        <tbody>
                                            <tr>
                                                <td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding: 25px 15px 25px 15px; vertical-align: middle;">
                                                    <h2 style="margin: 0; color: #000000; font-family: Arial, Helvetica, sans-serif; font-size: 24px; font-weight: 700; text-align: center; margin-bottom: 15px;">Your Call is Confirmed!</h2>
                                                    <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center; margin-bottom: 5px;">Hi {full_name},</p>
                                                    <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center;">This email confirms your 'Project Pipeline AI' onboarding call is booked for:</p>
                                                    <p style="margin: 0; color:#5b0202; font-family:Arial, Helvetica, sans-serif; font-size:18px; font-weight: bold; text-align: center; margin-top: 10px; margin-bottom: 15px;">{start_time}</p>
                                                    <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center; margin-bottom: 25px;">You will receive a separate Google Calendar invitation shortly with the video call details.</p>
                                                     <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center; margin-top: 25px;">We're excited to connect with you!</p>
                                                     <p style="margin: 0; color:#000000; font-family:Arial, Helvetica, sans-serif; font-size:16px; text-align: center; margin-top: 10px;">Best,<br>The Zappies AI Team</p>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                     <table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                        <tbody><tr><td><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; color: #000000; width: 540px; margin: 0 auto;" width="540"><tbody><tr><td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top;"><div class="spacer_block block-1" style="height:60px;line-height:60px;font-size:1px;">&#8202;</div></td></tr></tbody></table></td></tr></tbody>
                    </table>
                </td>
            </tr>
        </tbody>
    </table>
</body>
</html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logger.info(f"Direct confirmation email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send direct confirmation email: {e}", exc_info=True)
        return False