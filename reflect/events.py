from flask import jsonify
from api import get_message, slack_api
from utils import block
from storage import reflect, recall


def url_verification_event(request):
    parsed = request.json
    challenge = parsed['challenge']
    return jsonify({"challenge": challenge})


def reaction_added_event(request):
    parsed = request.json
    team_id = parsed['team_id']
    event = parsed['event']
    if event['reaction'] in ('ididit', 'udidit'):
        item = event['item']
        event_user_id = event['user']
        if item['type'] == 'message':
            channel = item['channel']
            msg_ts = item['ts']
            msg_resp = get_message(team_id, channel, msg_ts)
            msg = msg_resp['messages'][0]
            msg_team_id, msg_user_id, text  = msg['team'], msg['user'], msg['text']
            if event['reaction'] == 'ididit':
                reflect(msg_team_id, msg_user_id, text)
            elif event['reaction'] == 'udidit':
                reflect(msg_team_id, event_user_id, text)
    return "Ok"

def app_home_opened_event(request):
    parsed = request.json
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
    resp = slack_api(team_id, "views.publish", msg)
    return "OK"
