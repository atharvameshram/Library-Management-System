from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def emailsender(elist):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailids = ', '.join(elist)
    emailMsg = 'Today is the last date for returning your book.\nKindly return the book at the library.'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = emailids
    mimeMessage['subject'] = 'Due Date for Returning Book'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
