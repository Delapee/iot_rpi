import ssl
import smtplib
import os
from email.message import EmailMessage


def send_mail(subject, body):
    em = EmailMessage()
    em["From"] = os.getenv("EMITER")
    em["To"] = os.getenv("RECEPTOR")
    em["Subject"] = subject
    em.set_content(body)

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
        smtp.login(os.getenv("EMITER"), os.getenv("PASS"))
        smtp.sendmail(os.getenv("EMITER"), os.getenv("RECEPTOR"), em.as_string())
