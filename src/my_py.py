"""
Simple Python template file allowing users to define intent resposnes (convention is lowercase
intent name from your intentsSchema and Utterances) as a function; leaving all the lambda skill
service details to the alexa_py.py file.

Intents implemented here for example:
  About
  Contact
  Upcoming

Intents supported by default (but to be filled in with your info):
  Open 
  AMAZON.HelpIntent
  AMAZON.CancelIntent or AMAZON.StopIntent


"""

import logging

# --------------- Your functions to implement your intents ------------------

def about():
    return "<speak>Welcome to ACME Inc. We are the coolest company located in the Silicon Valley of the South. We love our employees, customers, and the environment.</speak>"

def contact():
    return "<speak>The best way to reach us is at info at acme dot com. You can also leave us voice mail at 8 0 4, 5 5 5, 1 2 1 2. We are also on twitter, at acme S V O S.</speak>"

def upcoming():
    return "<speak>Check us out at Stir Trek dot com. We will be in Columbus, Ohio on May  5th!</speak>"


# --------------- Primary/Required functions (update as needed) ------------------

def launch():
    """ Called when the user launches the skill without specifying what they want
    """

    return "<speak>Welcome to the 411 for ACME Inc. This skill provides information about ACME, a really cool company located in Silicon Valley of the South.</speak>"


def help():
    """ Called when the user asks for help
    """

    return "<speak>This skill provides some basic information about ACME. You can ask for our location, contact info, and upcoming events.</speak>"


def end():

    return "<speak.Thank you for asking about our business. Have a nice day! </speak>"

