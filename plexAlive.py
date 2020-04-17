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
    to_number = '***PHONE NUMBER***{}'.format(carriers['att'])
    auth = ('***EMAIL***@gmail.com', '***PASSWORD***')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)


def checkAlive():
    server = "***PLEX SERVER IP ADDRESS***"
    port = 32400
    global isUp

    logging.basicConfig(filename='PlexServerCheck.log', level=logging.DEBUG)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((server, port))
    if result == 0:
        if isUp == False:
            send("Your Plex server is back up")
            isUp = True
        message = "Plex Server is alive: " + datetime.now().__str__()
        logging.info(message)
    else:
        if isUp == True:
            send("Your Plex server is down")
            isUp = False
        message = "Plex Server down at: " + datetime.now().__str__() + " Attempting to restart"
        logging.warning(message)
        # kill plex srever process if running
        subprocess.run(["killall", "\"Plex Media Server\""])
        # restart plex server
        subprocess.getoutput("open ~/Applications/Plex\\ Media\\ Server.app/")
    sock.close()


while True:
    checkAlive()
    time.sleep(sleepTime)

