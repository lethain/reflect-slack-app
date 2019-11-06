"""
Simple Slack application to track accomplishments.

See https://github.com/lethain/reflect-slack-app
    https://lethain.com/creating-reflect-slack-app/

"""
import os, logging, hmac, hashlib
from flask import escape, jsonify


def verify(request,secret):
    body = request.get_data()
    timestamp = request.headers['X-Slack-Request-Timestamp']
    sig_basestring = 'v0:%s:%s' % (timestamp, body.decode('utf-8'))
    computed_sha = hmac.new(secret, sig_basestring.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    my_sig = 'v0=%s' % (computed_sha,)
    slack_sig = request.headers['X-Slack-Signature']
    if my_sig != slack_sig:
        raise Exception("my_sig %s does not equal slack_sig %s" % (my_sig, slack_sig))


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
