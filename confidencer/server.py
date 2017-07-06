"""A simple server to deliver compliment texts on demand, using Twilio.

    This is an example project for Hacking for Humanity 2017.

    (c) 2017 Hackbright Academy
"""

from twilio.rest import Client


# a Client constructor without account and token parameters will look for 
# TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN variables inside the current 
# environment.
# 
# These are added to the environment by sourcing a secrets.sh file (not included
# in this repo because contents are a secret!)
# 
# The secrets.sh file contents look like this: 
# 
#   export TWILIO_ACCOUNT_SID="xxxxxxx"
#   export TWILIO_AUTH_TOKEN="xxxxxxx"
# 
# With the xxxxxxx replaced with the account and token generated from 
# https://www.twilio.com/try-twilio 
# 
# Then run 
#   source secrets.sh
# from the command line to bring the environment variables into the environment.

client = Client()
