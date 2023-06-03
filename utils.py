import argparse
import qrcode
import random
import string
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.message import EmailMessage
import os
import io

pd.set_option("mode.chained_assignment", None)


# Generate random IDs for attendees
def generate_id(attendee):
    letters = string.ascii_lowercase
    attendee_id = "".join(random.choice(letters) for i in range(5))

    df = pd.read_excel("output.xlsx")
    df["ID"][df["BUSINESS EMAIL"] == attendee["BUSINESS EMAIL"]] = attendee_id
    df.to_excel("output.xlsx", index=False)

    return attendee_id


def generate_qr(attendee, ip_address):
    # Generate attendee ID and save to file
    attendee_id = generate_id(attendee)

    # Generate QR code with attendee ID and Flask server URL
    url = f"http:/{ip_address}:5000/verify"
    data = f"attendee_id: {attendee_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"{url}?id={attendee_id}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to an in-memory buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    qr_image = buffer.read()
    return qr_image


def send_email(attendee, subject, qr_image=None):
    # Create message object
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = os.getenv("APP_EMAIL")
    msg["To"] = attendee["BUSINESS EMAIL"]

    body = f'Dear {attendee["FIRST NAME"]} {attendee["LAST NAME"]}, please find your QR code attached. Please scan this code at the entrance of the event to gain access. Thank you!'

    # Attach QR code image to email body
    if qr_image:
        image = MIMEImage(qr_image)
        image.add_header("Content-ID", "<qr_code>")
        image.add_header("Content-Disposition", "inline", filename="qr_code.png")
        msg.attach(image)
        body += "<br><img src='cid:qr_code'>"

    # Attach text message to email body
    text = MIMEText(body, "html")
    msg.attach(text)

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(os.getenv("APP_EMAIL"), os.getenv("APP_PASSWORD"))

        smtp.sendmail(msg["From"], msg["To"], msg.as_string())
