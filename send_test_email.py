# send_test_email.py

import smtplib
from email.message import EmailMessage
import os
import sys
from email.utils import formataddr

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
TO_ADDRESS = os.getenv('EMAIL_TO')

# Create a text/plain message
msg = EmailMessage()
msg['Subject'] = 'eXpresso0.3'
msg["From"] = formataddr(("Morning EXpresso", EMAIL_ADDRESS))
msg['To'] = TO_ADDRESS
msg.set_content('{}\n{}'.format(sys.argv[1],sys.argv[2]))


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

