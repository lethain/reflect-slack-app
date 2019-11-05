"""
Simple Slack application to track accomplishments.

See https://github.com/lethain/reflect-slack-app
    https://lethain.com/creating-reflect-slack-app/

"""
import logging
from flask import escape, jsonify


def reflect_post(request):
    data = request.form
    return "Reflected: `{}`".format(data['text'])


def recall(team_id, user_id, text):
    "Recall reflections for (`team_id`, `user_id`) filtered by parameters in `text`"
    # stub implementation
    import random
    return ["I did something {}".format(x) for x in range(random.randint(3, 10))]


def block(typ, text=None):
    if typ == "mrkdwn":
        return {
            "type": "section",
            "text": {
                "text": text,
                "type": "mrkdwn"
            }
        }
    else:
        return {
            "type": typ
        }
    return data

def recall_post(request):
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