import wmi
import smtplib
import cv2
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import psutil
from datetime import datetime, timezone

MAX_FAILED_ATTEMPTS = 3
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "yoursenderemail@gmail.com"
SENDER_PASSWORD = "yourgmailAPP-password"
RECIPIENT_EMAIL = "yourrecipientemail"

def adjust_brightness(image, alpha=1.5, beta=50):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def capture_photo():
    try:
        images_folder = os.path.join(os.path.expanduser("~"), "Pictures")
        photo_path = os.path.join(images_folder, "intruder.jpg")

        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        cam = cv2.VideoCapture(0)
        cam.set(3, 1920)
        cam.set(4, 1080)
        cam.set(cv2.CAP_PROP_GAMMA, 200)
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        cam.set(cv2.CAP_PROP_FOCUS, 50)
        cam.set(cv2.CAP_PROP_EXPOSURE, -4)
        time.sleep(3)
        ret, frame = cam.read()
        if ret:
            frame = adjust_brightness(frame)
            cv2.imwrite(photo_path, frame)
        else:
            print("Error: Could not read from the camera.")
        cam.release()
        cv2.destroyAllWindows()
        return photo_path
    except Exception as e:
        print(f"Error capturing photo: {e}")
        return None

def send_alert_email(photo_path):
    if not SENDER_EMAIL or not SENDER_PASSWORD or not RECIPIENT_EMAIL:
        print("Email credentials not set. Please configure environment variables.")
        return
    
    subject = "Warning! Several Malicious Login Attempts On Your System"
    body = "Someone is trying to log in. Check the attached photo."

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if photo_path and os.path.exists(photo_path):
        with open(photo_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(photo_path)}")
            msg.attach(part)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def get_system_boot_time():
    boot_timestamp = psutil.boot_time()
    return datetime.fromtimestamp(boot_timestamp, tz=timezone.utc)

def monitor_failed_logins():
    c = wmi.WMI()
    failed_count = 0
    boot_time = get_system_boot_time()

    print("Boot Time:", boot_time)

    events = c.Win32_NTLogEvent(Logfile="Security", EventCode=4625)
    print(f"Total failed login events found: {len(events)}")

    for event in events:
        event_time = datetime.strptime(event.TimeGenerated.split('.')[0], "%Y%m%d%H%M%S")
        event_time = event_time.replace(tzinfo=timezone.utc)
        print(f"Event Time: {event_time}")

        if event_time >= boot_time:
            failed_count += 1
            print(f"[ALERT] Failed login attempt detected! Count: {failed_count}")

            if failed_count >= MAX_FAILED_ATTEMPTS:
                print("[⚠️] Intruder detected! Capturing photo and sending email...")
                time.sleep(1)
                photo_path = capture_photo()
                send_alert_email(photo_path)
                return

if __name__ == "__main__":
    monitor_failed_logins()
