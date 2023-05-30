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

pd.set_option("mode.chained_assignment", None)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip", type=str, default="localhost", help="IP address for Flask server"
    )
    parser.add_argument(
        "--subject", type=str, required=True, help="Subject of the emails"
    )
    parser.add_argument(
        "--excel_path", type=str, required=True, help="Path to attendance list excel"
    )
    return parser.parse_args()


# Generate random IDs for attendees
def generate_id(attendee):
    letters = string.ascii_lowercase
    attendee_id = "".join(random.choice(letters) for i in range(5))
    df = pd.read_excel("output.xlsx")
    df["ID"][df["BUSINESS EMAIL"] == attendee["BUSINESS EMAIL"]] = attendee_id
    df.to_excel("output.xlsx", index=False)
    # with open("attendee_ids.txt", "a") as f:
    #     f.write(f"{attendee_id}\n")
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
    img.save(f"qr_codes/{attendee_id}.png")

    with open(f"qr_codes/{attendee_id}.png", "rb") as f:
        qr_image = f.read()
        return qr_image

    return None


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


if __name__ == "__main__":
    # Read email addresses from Excel file
    args = parse_arguments()
    attendees_df = pd.read_excel(f"{args.excel_path}.xlsx", skiprows=3)

    attendees_df["SHOW"] = "NO"
    attendees_df["ID"] = ""
    attendees_df.fillna("", inplace=True)
    attendees_df["MOBILE NUMBER"] = attendees_df["MOBILE NUMBER"].astype(str)
    attendees_df.to_excel("output.xlsx", index=False)

    print("Sending email from: ", os.getenv("APP_EMAIL"))

    for _, row in attendees_df.iterrows():
        if row["BUSINESS EMAIL"] != "":
            qr = generate_qr(row, args.ip)
            send_email(row, args.subject, qr)

    print("Emails sent succesfully!")
