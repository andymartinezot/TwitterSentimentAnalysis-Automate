import os
import smtplib
from email.message import EmailMessage
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
    
EMAIL_ADDRESS = "andytesting361@gmail.com"
EMAIL_PASSWORD = "your_password"

def send_mail(email, password):

    msg = EmailMessage()
    msg['Subject'] = "Twitter Sentiment Analysys"
    msg['From'] = email
    msg['To'] = ['mail_to_send']

    msg.set_content('Attached is the report and csv about the sentiment behaviour.')
    files = ['TweetsAnalized.csv','TweetsReport.pdf']

    for f in files:
        with open(f, 'rb') as f:
            data = f.read()
            file_name = f.name
            msg.add_attachment(data, maintype='application',subtype='octetc-stream',filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)

#send_mail(EMAIL_ADDRESS, EMAIL_PASSWORD)