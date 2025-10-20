# --- ADD THIS FUNCTION TO THE END OF tools/email_sender.py ---

def send_direct_booking_confirmation(recipient_email: str, full_name: str, start_time: str):
    """
    Sends a direct meeting confirmation email (no link) for synchronous bookings
    (e.g., from the voice agent).
    """
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_APP_PASSWORD
    
    if not sender_email or not sender_password:
        logger.error("Sender email or password not configured. Cannot send direct confirmation email.")
        return False

    # Create the email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Your Onboarding Call with Zappies AI is Confirmed!"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Simple HTML body for the direct confirmation
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <p>Hi {full_name},</p>
        <p>This email is to confirm that your 'Project Pipeline AI' onboarding call has been successfully booked for <strong>{start_time}</strong>.</p>
        <p>You will receive a separate Google Calendar invitation shortly with the video call link.</p>
        <p>We're excited to connect with you!</p>
        <p>Best,<br>The Zappies AI Team</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logger.info(f"Direct confirmation email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send direct confirmation email: {e}", exc_info=True)
        return False