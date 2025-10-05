# send_test_email.py

import smtplib
from email.message import EmailMessage
import os

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
TO_ADDRESS = os.getenv('EMAIL_TO')

msg = EmailMessage()
msg['Subject'] = 'Test Email from GitHub Actions'
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_ADDRESS
msg.set_content("This is a test email sent from a GitHub Actions workflow. If you're reading this, it worked!")

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

