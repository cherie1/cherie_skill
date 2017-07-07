"""
Simple Python Lambda service that uses a simplified my_py.py file to provide simple
responses to simple "fact"-like intents. The example my_py.py with this repo supports
the following:

Intents supported:

  Custom:
    About
    Contact
    Upcoming

  Required:
    LaunchRequest (request type that calls launch function in my_py)
    AMAZON.HelpIntent (intent that calls help function in my_py)
    AMAZON.CancelIntent or AMAZON.StopIntent (intent, both use end function in my_py)

Note, that as long as you keep your intents in sync with your skill intentSchema, you can
simply update or add intents as functions to the my_py.py and the lambda service will use them.
Intents in your Schema may be mixed case -- this code will convert to lower case.

Furthermore, using this template will make it easier to make an external API call or DB call
to form the response. If you want to stick to simply updating text, you can try out the S3
branch where you can update the responses in a JSON file (no code).

Further note, there is .travis.yml in this repo that does two things:
  1) Deploys this code to your configured lambda function.
  2) Deploys the ../responses/response.json to your bucket.

If you fork this repo or create your own copy and keep it as a public repo, you can use
Travis to deploy to your lambda. You'll want to change the following configs:

  in deploy-provider: lambda
    function_name
    role
    access_key_id (available from AWS console)
    secret_access_key (also available from AWS console, but make sure you use travis command
    line to encrypt your key)


"""

import logging
import my_py

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# Function which delegates the speech output for the response based on the JSON file.
# Simply looking up the intent in the responses map created from the parsed JSON.
#
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    session_attributes = {} # No session attributes needed for simple fact response
    reprompt_text = None # No reprompt text set
    speech_output = ""
    should_end_session = True # Can end session after fact is returned (no additional dialogue)

    if intent_name == "launch":
        should_end_session = False # Opening a skill requires the session remain open
    elif intent_name == "AMAZON.HelpIntent":
        should_end_session = False # Asking for help requires the session remain open
        intent_name = 'help'
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        intent_name = 'end'
    else:
        intent_name = intent_name.lower()

    # Grab the response specified for the given intent of the JSON by calling
    # the function defined in my_py
    speech_output = getattr(my_py,intent_name)()

    return build_response(session_attributes, build_speechlet_response
                          (intent_name,speech_output,reprompt_text,should_end_session))

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    logger.info("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    # I am injecting a new "intent" type of launch in order to
    # allow my_py to provide the response text for a LaunchRequest
    if event['request']['type'] == "LaunchRequest":
        event['request']['intent'] = { 'name':'launch' }
    
    return on_intent(event['request'], event['session'])

