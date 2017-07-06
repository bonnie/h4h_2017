"""A file containing Twilio helper functions for the Confidencer app."""

# for environment variable secrets
import os

# for regular expressions
import re

# for the twilio python wrapper
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

# get the "from" phone number from the environment (also in secrets.sh)
FROM_PHONE = os.environ.get("FROM_PHONE")


def send_sms(msg, phone_num):
    """Send msg as an SMS text message to phone_num.

    arguments: 
        msg: string containing text message to send
        phone_num: string containing a phone number.
            * see parse_phone docstring for acceptable formats

    returns:
        dict with the following keys: 
            "success": boolean, whether or not the sms was sent successfully
            "error": string, only populated if there was an error sending the text

    """

    phone = parse_phone(phone_num)
    if not phone: 
        # the phone number wasn't in the proper format
        return {
            "success": False, 
            "message": "{} is not a readable phone number".format(phone_num)
        }

    message = client.messages.create(
        to=phone,
        from_=FROM_PHONE,
        body=msg)

    # message is an object that will have a None error_code attribute and None 
    # error_message attribute if the sms is successful. Otherwise there will be
    # useful info in those attributes. 
    if message.error_message:
        return {
            "success": False, 
            "message": "Twilio SMS failure: {}".format(message.error_message)
        }

    # if we got to here, all's well
    return {
        "success": True,
        "message": ""
    }


def parse_phone(phone_num):
    """Takes a phone number in a variety of formats and returns 10 digits.

    arguments: 
        phone_num: string containing a phone number, in one of these formats: 
            (555) 555-5555
            (555)555-5555
            555-555-5555
            5555555555

    returns:
        string of 10 digits (neglecting errors for now), or None if error.

    Examples / doctests:

        >>> print parse_phone("(555) 555-5555")
        5555555555

        >>> print parse_phone("(555)555-5555")
        5555555555

        >>> print parse_phone("555-555-5555")
        5555555555

        >>> print parse_phone("555555-5555")
        5555555555

        >>> print parse_phone("(555) 555-55555")
        None

    """

    # a somewhat obscure regular expression to get the data out of the phone
    # number in various formats. (see http://regex101.com for more details on 
    # -- and a sandbox for -- regular expressions.)
    matches = re.match(r'^\(?(\d{3})\)?[\s\-]?(\d{3})-?(\d{4})$', phone_num)

    if not matches: 
        # the phone number wasn't in one of the acceptable formats
        return None

    # get the data from the regular expression
    # for more details, see 
    # https://docs.python.org/2/library/re.html#match-objects
    area_code = matches.group(1)
    exchange = matches.group(2)
    other_part = matches.group(3)
    return "{}{}{}".format(area_code, exchange, other_part)

