# tools/email_sender.py
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_confirmation_email(recipient_email: str, full_name: str, start_time: str, meeting_id: str):
    """Sends a meeting confirmation email using SMTP."""
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_APP_PASSWORD
    
    if not sender_email or not sender_password:
        logger.error("Sender email or password not configured. Cannot send email.")
        return False

    confirmation_url = f"{settings.API_BASE_URL}/confirm-meeting/{meeting_id}"
    
    # Create the email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Please Confirm Your Onboarding Call with Zappies AI"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    html_body = f"""
    <html>
    <body>
        <p>Hi {full_name},</p>
        <p>Thanks for booking your 'Project Pipeline AI' onboarding call for <strong>{start_time}</strong>.</p>
        <p>To secure your spot, please click the link below to confirm your attendance:</p>
        <p><a href="{confirmation_url}" style="padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Confirm Your Meeting</a></p>
        <p>We're excited to connect with you!</p>
        <p>Best,<br>The Zappies AI Team</p>
    </body>
    </html>
    """
    html_body = """
<!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">

<head>
	<title></title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0"><!--[if mso]>
<xml><w:WordDocument xmlns:w="urn:schemas-microsoft-com:office:word"><w:DontUseAdvancedTypographyReadingMail/></w:WordDocument>
<o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml>
<![endif]--><!--[if !mso]><!--><!--<![endif]-->
	<style>
		* {
			box-sizing: border-box;
		}

		body {
			margin: 0;
			padding: 0;
		}

		a[x-apple-data-detectors] {
			color: inherit !important;
			text-decoration: inherit !important;
		}

		#MessageViewBody a {
			color: inherit;
			text-decoration: none;
		}

		p {
			line-height: inherit
		}

		.desktop_hide,
		.desktop_hide table {
			mso-hide: all;
			display: none;
			max-height: 0px;
			overflow: hidden;
		}

		.image_block img+div {
			display: none;
		}

		sup,
		sub {
			font-size: 75%;
			line-height: 0;
		}

		@media (max-width:560px) {
			.desktop_hide table.icons-inner {
				display: inline-block !important;
			}

			.icons-inner {
				text-align: center;
			}

			.icons-inner td {
				margin: 0 auto;
			}

			.mobile_hide {
				display: none;
			}

			.row-content {
				width: 100% !important;
			}

			.stack .column {
				width: 100%;
				display: block;
			}

			.mobile_hide {
				min-height: 0;
				max-height: 0;
				max-width: 0;
				overflow: hidden;
				font-size: 0px;
			}

			.desktop_hide,
			.desktop_hide table {
				display: table !important;
				max-height: none !important;
			}

			.row-3 .row-content {
				padding: 0 !important;
			}

			.row-3 .column-1 {
				padding: 5px 0 !important;
			}
		}
	</style><!--[if mso ]><style>sup, sub { font-size: 100% !important; } sup { mso-text-raise:10% } sub { mso-text-raise:-10% }</style> <![endif]--><!--[if true]><style>.forceBgColor{background-color: white !important}</style><![endif]-->
</head>

<body class="body forceBgColor" style="background-color: transparent; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
	<table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: transparent; background-image: none; background-position: top left; background-size: auto; background-repeat: no-repeat;">
		<tbody>
			<tr>
				<td>
					<table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
						<tbody>
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
																	<div style="max-width: 81px;"><img src="https://ab8565207c.imgdist.com/pub/bfra/a9yo6qej/hp6/5nn/xlp/favicon.png" style="display: block; height: auto; border: 0; width: 100%;" width="81" alt title height="auto"></div>
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
						</tbody>
					</table>
					<table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 19px; color: #000000; width: 540px; margin: 0 auto;" width="540">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-left: 5px; padding-right: 5px; padding-top: 5px; vertical-align: top;">
													<table class="heading_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
														<tr>
															<td class="pad" style="text-align:center;width:100%;">
																<h2 style="margin: 0; color: #000000; direction: ltr; font-family: Arial, Helvetica, sans-serif; font-size: 30px; font-weight: 700; letter-spacing: normal; line-height: 1.2; text-align: center; margin-top: 0; margin-bottom: 0; mso-line-height-alt: 36px;"><span class="tinyMce-placeholder" style="word-break: break-word;">Confirm Your Onboarding Call&nbsp;</span></h2>
															</td>
														</tr>
													</table>
													<table class="heading_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
														<tr>
															<td class="pad" style="padding-left:15px;padding-right:15px;padding-top:15px;text-align:center;width:100%;">
																<h5 style="margin: 0; color: #5b0202; direction: ltr; font-family: Arial, Helvetica, sans-serif; font-size: 20px; font-weight: 700; letter-spacing: normal; line-height: 1.2; text-align: center; margin-top: 0; margin-bottom: 0; mso-line-height-alt: 24px;"><span class="tinyMce-placeholder" style="word-break: break-word;">"""+full_name+"""</span></h5>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-bottom: 1px solid #e2e2e2; border-left: 1px solid #e2e2e2; border-radius: 20px; border-right: 1px solid #e2e2e2; border-top: 1px solid #e2e2e2; color: #000000; width: 540px; margin: 0 auto;" width="540">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: middle;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
														<tr>
															<td class="pad" style="padding-top:15px;">
																<div style="color:#000000;direction:ltr;font-family:Arial, Helvetica, sans-serif;font-size:18px;font-weight:400;letter-spacing:0px;line-height:1.2;text-align:center;mso-line-height-alt:22px;">
																	<p style="margin: 0;">Thanks for booking your 'Project Pipeline AI' onboarding call for</p>
																</div>
															</td>
														</tr>
													</table>
													<table class="paragraph_block block-2" width="100%" border="0" cellpadding="15" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
														<tr>
															<td class="pad">
																<div style="color:#5b0202;direction:ltr;font-family:Arial, Helvetica, sans-serif;font-size:18px;font-weight:400;letter-spacing:0px;line-height:1.2;text-align:center;mso-line-height-alt:22px;">
																	<p style="margin: 0;"><strong>"""+start_time+"""</strong></p>
																</div>
															</td>
														</tr>
													</table>
													<table class="paragraph_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
														<tr>
															<td class="pad">
																<div style="color:#000000;direction:ltr;font-family:Arial, Helvetica, sans-serif;font-size:18px;font-weight:400;letter-spacing:0px;line-height:1.2;text-align:center;mso-line-height-alt:22px;">
																	<p style="margin: 0;">To secure your spot, please click the link below to confirm your attendance:</p>
																</div>
															</td>
														</tr>
													</table>
													<table class="button_block block-4" width="100%" border="0" cellpadding="40" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
														<tr>
															<td class="pad">
																<div class="alignment" align="center"><a href=" """+confirmation_url+""" " target="_blank" style="color:#fff1dd;text-decoration:none;"><!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word"  href=" """+confirmation_url+""" "  style="height:50px;width:232px;v-text-anchor:middle;" arcsize="8%" fillcolor="#5b0202">
<v:stroke dashstyle="Solid" weight="0px" color="#5b0202"/>
<w:anchorlock/>
<v:textbox inset="0px,0px,0px,0px">
<center dir="false" style="color:#fff1dd;font-family:sans-serif;font-size:20px">
<![endif]--><span class="button" style="background-color: #5b0202; mso-shading: transparent; border-bottom: 0px solid transparent; border-left: 0px solid transparent; border-radius: 4px; border-right: 0px solid transparent; border-top: 0px solid transparent; color: #fff1dd; display: inline-block; font-family: Arial, Helvetica, sans-serif; font-size: 20px; font-weight: 400; mso-border-alt: none; padding-bottom: 5px; padding-top: 5px; padding-left: 20px; padding-right: 20px; text-align: center; width: auto; word-break: keep-all; letter-spacing: normal;"><span style="word-break: break-word; line-height: 40px;">Confirm Your Meeting</span></span><!--[if mso]></center></v:textbox></v:roundrect><![endif]--></a></div>
															</td>
														</tr>
													</table>
													<table class="paragraph_block block-5" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
														<tr>
															<td class="pad">
																<div style="color:#000000;direction:ltr;font-family:Arial, Helvetica, sans-serif;font-size:16px;font-weight:400;letter-spacing:0px;line-height:1.2;text-align:center;mso-line-height-alt:19px;">
																	<p style="margin: 0; margin-bottom: 16px;">We're excited to connect with you!</p>
																	<p style="margin: 0;">Thanks,<br>The Zappies AI Team</p>
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
						</tbody>
					</table>
					<table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; color: #000000; width: 540px; margin: 0 auto;" width="540">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top;">
													<div class="spacer_block block-1" style="height:60px;line-height:60px;font-size:1px;">&#8202;</div>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-5" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 540px; margin: 0 auto;" width="540">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top;">
													<table class="icons_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; text-align: center; line-height: 0;">
														<tr>
															<td class="pad" style="vertical-align: middle; color: #1e0e4b; font-family: 'Inter', sans-serif; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;"><!--[if vml]><table align="center" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
																<!--[if !vml]><!-->
																<table class="icons-inner" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; padding-left: 0px; padding-right: 0px;" cellpadding="0" cellspacing="0" role="presentation"><!--<![endif]-->
																</table>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
				</td>
			</tr>
		</tbody>
	</table><!-- End -->
</body>

</html>
    """
    
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logger.info(f"Confirmation email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {e}", exc_info=True)
        return False
    
def send_handover_email(conversation_id: str, history: list):
    """Sends a human handover notification with the chat history."""
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_APP_PASSWORD
    recipient_email = settings.HANDOVER_EMAIL

    if not all([sender_email, sender_password, recipient_email]):
        logger.error("Email configuration is incomplete. Cannot send handover email.")
        return False

    # Format the chat history into a readable HTML string
    history_html = ""
    for message in history:
        speaker = "User" if message.type == 'human' else "AI"
        # Sanitize message content for HTML
        import html
        content = html.escape(message.content)
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
        <div style="background-color: #f4f4f4; border-left: 3px solid #ccc; padding: 10px;">
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