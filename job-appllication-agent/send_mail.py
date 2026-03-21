import smtplib
import os
import json
import time

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")

def send_mail(recipient_email, subject, body, attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            filename = os.path.basename(attachment_path)
            
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename={filename}",
            )
        
            msg.attach(part)
    
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
    except Exception as e:
        print("Error occured while sending email", e)
    else:
        print("[+] Resume Sent :", recipient_email)

# load contacts file
with open("generated_emails.json", "r") as file:
    data = json.load(file)

# send mail to each hr present in the file
for hr in data:
    send_mail(
        recipient_email=hr["hr_email"],
        subject=hr["subject"],
        body=hr["body"],
        attachment_path="./resume.pdf"
    )

    time.sleep(150) # wait for 5 minute before sending another email