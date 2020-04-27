# plexAlive
Check to see if Plex server is up.

Script checks every 3 minutes to see if Plex server is up and running.
If server goes down, script will attempt to reboot the service.

Text notifications can be sent via email routing.
  - Text will be sent when server goes down the first time.
  - Text will be sent when server goes back up after down state
  
## To Run
Make sure you are running [python3](https://realpython.com/installing-python/) on your system.

1. Search and replace all fields in the script beginning with *** :

   - ***PHONE NUMBER*** : Phone number to receive text if server goes down/back up
   - ***EMAIL*** : email is required for text message routing
   - ***PASSWORD*** : email account password
   - ***SERVER IP*** : IP address of Plex server host

For email, I recommend creating a dummy account so you can turn on [access to less secure apps](https://support.google.com/accounts/answer/6010255?hl=en)

2. `python3 plexAlive.py`
or
`python3 plexAlive.py &` to run in background

## Logging
Script will log the state of server every 3 minutes to PlexServerCheck.log
