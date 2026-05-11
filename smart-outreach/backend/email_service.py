import smtplib
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def attach_resume(msg):
    resume_path = Path(__file__).resolve().parent / "resume.pdf"
    if not resume_path.exists():
        raise FileNotFoundError(f"Missing resume file at: {resume_path}")
    with open(resume_path, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename="resume.pdf"'
        )
        msg.attach(part)

def send_email(to_email, subject, body, smtp_email=None, smtp_password=None):
    sender = smtp_email or os.getenv("SMTP_EMAIL")
    password = smtp_password or os.getenv("SMTP_APP_PASSWORD")
    if not sender or not password:
        raise ValueError("Set SMTP_EMAIL and SMTP_APP_PASSWORD in backend environment.")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attach_resume(msg)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, password)
    server.send_message(msg)
    server.quit()