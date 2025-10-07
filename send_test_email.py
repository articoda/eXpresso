# send_test_email.py

import smtplib
from email.message import EmailMessage
import os

# Open the plain text file whose name is in textfile for reading.
with open('body.txt') as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())


EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
TO_ADDRESS = os.getenv('EMAIL_TO')

msg['Subject'] = 'Test Email Number 2 from GitHub Actions'
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_ADDRESS

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

