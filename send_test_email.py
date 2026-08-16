# send_test_email.py

import smtplib
from email.message import EmailMessage
import os
import sys
from email.utils import formataddr

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
TO_ADDRESS = os.getenv('EMAIL_TO')
SENDER_NAME = os.getenv('SENDER_NAME', 'Morning eXpresso')
EMAIL_SUBJECT = os.getenv('EMAIL_SUBJECT', 'eXpresso')

missing = [
    name for name, value in {
        'EMAIL_USER': EMAIL_ADDRESS,
        'EMAIL_PASS': EMAIL_PASSWORD,
        'EMAIL_TO': TO_ADDRESS,
    }.items() if not value
]
if missing:
    raise RuntimeError('Missing required environment variable(s): ' + ', '.join(missing))

# Create a text/plain message
msg = EmailMessage()
msg['Subject'] = EMAIL_SUBJECT
msg["From"] = formataddr((SENDER_NAME, EMAIL_ADDRESS))
msg['To'] = TO_ADDRESS
msg.set_content('{}\n{}'.format(sys.argv[1],sys.argv[2]))


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

