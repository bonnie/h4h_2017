# This Python file uses the following encoding: utf-8
"""A simple server to deliver compliment texts on demand, using Twilio.

    This is an example project for Hacking for Humanity 2017.

    (c) 2017 Hackbright Academy
"""

# for getting the flask secret from the environment
import os

# to get a random message
from random import choice

# for the web server
from flask import Flask, render_template, request, flash, redirect

# list of confidence boosters
from boosters import BOOSTERS

# function to send an sms message
from twilio_calls import send_sms


# instantiate the flask app
app = Flask(__name__)

# add a secret key to be able to use flash
app.secret_key = os.environ.get("FLASK_SECRET")


# the "root" route
@app.route("/")
def print_home():
    """Print the home page with a big button for a compliment."""

    return render_template("index.html")


@app.route("/confirmation")
def send_message():
    """Send the sms message and display a confirmation or error."""

    msg = choice(BOOSTERS)
    phone = request.args.get("phone")

    # attempt to send the message
    result = send_sms(msg, phone)

    if result["success"]: 
        # it worked! 
        flash("Success! You should get a text message shortly.")

    else:
        # it did not work
        flash("Couldn't sent the text message: {}".format(result["message"]))
        flash("Here's a web message just for you: {}".format(msg))

    return redirect("/")


if __name__ == '__main__':
    # if this is called directly

    app.run(port="5050")