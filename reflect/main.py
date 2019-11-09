"""
Simple Slack application to track accomplishments.

See https://github.com/lethain/reflect-slack-app
    https://lethain.com/creating-reflect-slack-app/

"""
import os, logging
from flask import jsonify
from api import get_message, slack_api
from utils import block, verify


def reflect(team_id, user_id, text):
    print("Reflected(%s, %s): %s" % (team_id, user_id, text))


def recall(team_id, user_id, text):
    "Recall reflections for (`team_id`, `user_id`) filtered by parameters in `text`"
    # stub implementation
    import random
    return ["I did something {}".format(x) for x in range(random.randint(3, 10))]    


def url_verification_event(request, parsed):
    challenge = parsed['challenge']
    return jsonify({"challenge": challenge})


def reaction_added_event(request, parsed):
    event = parsed['event']
    if event['reaction'] in ('ididit', 'udidit'):
        item = event['item']
        event_user_id = event['user']
        if item['type'] == 'message':
            channel = item['channel']
            msg_ts = item['ts']
            msg_resp = get_message(channel, msg_ts)
            msg = msg_resp['messages'][0]
            msg_team_id, msg_user_id, text  = msg['team'], msg['user'], msg['text']
            if event['reaction'] == 'ididit':
                reflect(msg_team_id, msg_user_id, text)
            elif event['reaction'] == 'udidit':
                reflect(msg_team_id, event_user_id, text)
    return "Ok"


def event_callback_event(request, parsed):
    event_type = parsed['event']['type']
    if event_type == 'app_home_opened':
        return app_home_opened_event(request, parsed)
    elif event_type == 'reaction_added':
        return reaction_added_event(request, parsed)
    else:
        raise Exception("unable to handle event_callback event type: %s" % (event_type,))


def app_home_opened_event(request, parsed):
    user_id = parsed['event']['user']
    team_id = parsed['team_id']
    items = recall(team_id, user_id, "last 14 days")
    items_text = "\n".join(["%s. %s" % (i, x) for i, x in enumerate(items, 1)])
    blocks_spec = [
        ('mrkdwn', "Your home tab for Reflect"),
        ('divider',),
        ('mrkdwn', items_text),
        ('divider',),
        ('mrkdwn', "Some more stuff here"),
    ]
    blocks = [block(*x) for x in blocks_spec]
    msg = {
        "user_id": user_id,
        "view": {
            "type": "home",
            "blocks": blocks,
        }
    }
    resp = slack_api("views.publish", msg)
    return "OK"


def event_post(request):
    signing_secret = os.environ['SLACK_SIGN_SECRET'].encode('utf-8')
    verify(request, signing_secret)
    parsed = request.json
    event_type = parsed['type']
    if event_type == 'url_verification':
        return url_verification_event(request, parsed)
    if event_type == 'event_callback':
        return event_callback_event(request, parsed)
    else:
        raise Exception("unable to handle event type: %s" % (event_type,))


def reflect_post(request):
    signing_secret = os.environ['SLACK_SIGN_SECRET'].encode('utf-8')
    verify(request, signing_secret)

    data = request.form
    team_id, user_id, text = data['team_id'], data['user_id'], data['text']
    reflect(team_id, user_id, text)
    return "Reflected: `{}`".format(text)


def recall_post(request):
    signing_secret = os.environ['SLACK_SIGN_SECRET'].encode('utf-8')
    verify(request, signing_secret)

    data = request.form
    team_id, user_id, text = data['team_id'], data['user_id'], data['text']
    items = recall(team_id, user_id, text)
    items_text = "\n".join(["%s. %s" % (i, x) for i, x in enumerate(items, 1)])

    block_args = [
        ('mrkdwn', "Recalling `{}`".format(text)),
        ('divider',),
        ('mrkdwn', items_text),
        ('divider',),
        ('mrkdwn', "_Trying filtering by tag and date_ `/recall last 7 days #mgmt`."),
        ('mrkdwn', "_Share your response with the room by adding `public` anywhere in your response_"),
    ]
    resp = {
        "text": items_text,
        "response_type": "in_channel" if "public" in text else "ephemeral",
        "blocks": [block(*args) for args in block_args]
    }
    return jsonify(resp)
