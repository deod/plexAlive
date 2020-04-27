# check to see that plex server is up and running

import socket
from datetime import datetime
import logging
import subprocess
import time
import smtplib

carriers = {
    'att':    '@mms.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}
# Global variable to check if server switched betweeen running/down
isUp = True
# 3 minute intervals
sleepTime = 180

# function for sending text message
def send(message):
    # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = '***PHONE NUMBER8***{}'.format(carriers['att'])
    auth = ('***EMAIL***@gmail.com', '***PASSWORD***')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)

# bring plex back up
def restartPlex():
    # restart wifi
    logging.info("Restarting Wi-Fi")
    subprocess.run(["networksetup","-setairportpower", "en1", "off"])
    time.sleep(2)
    subprocess.run(["networksetup","-setairportpower", "en1", "on"])
    time.sleep(2)
    # kill plex srever process if running
    logging.info("Restarting Plex Server App")
    subprocess.run(["killall", "\"Plex Media Server\""])
    # restart plex server
    subprocess.getoutput("open ~/Applications/Plex\\ Media\\ Server.app/")

def checkAlive():
    server = "***SERVER IP***"
    port = 32400
    global isUp
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    currDateTime = datetime.now().__str__()

    logging.basicConfig(filename='PlexServerCheck.log', level=logging.DEBUG)
    try:
        result = sock.connect_ex((server, port))
        # if server is up
        if result == 0:
            message = "Plex Server is alive: " + currDateTime
            logging.info(message)

            if isUp == False:
                try:
                    send("Your Plex server is back up")
                except:
                    logging.error("Unable to send text message, check connectivity")
                finally:
                    isUp = True
        # if server is down
        else:
            message = "Plex Server down at: " + currDateTime + " Attempting to restart"
            logging.warning(message)

            restartPlex()

            if isUp == True:
                try:
                    send("Your Plex server is down")
                except:
                    logging.error("Unable to send text message, check connectivity")
                finally:
                    isUp = False
    except:
        logging.warning("Something when wrong checking server status at " + server + " at port "
                        + port.__str__() + " at " + currDateTime)
    finally:
        sock.close()


while True:
    checkAlive()
    time.sleep(sleepTime)

