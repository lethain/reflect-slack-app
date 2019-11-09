from flask import jsonify
from utils import block
from storage import reflect, recall


def reflect_command(request):
    data = request.form
    team_id, user_id, text = data['team_id'], data['user_id'], data['text']
    reflect(team_id, user_id, text)
    return "Reflected: `{}`".format(text)


def recall_command(request):
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
