import os
import requests


def get_message(channel, msg_ts):
    url = "https://slack.com/api/conversations.history"
    bot_token = os.environ['SLACK_OAUTH_TOKEN'].encode('utf-8')
    params = {
        'token': bot_token,
        'channel': channel,
        'latest': msg_ts,
        'limit': 1,
        'inclusive': True
    }
    resp = requests.get(url, params=params)
    return resp.json()


def slack_api(endpoint, msg):
    url = "https://slack.com/api/%s" % (endpoint,)
    bot_token = os.environ['SLACK_BOT_TOKEN'].encode('utf-8')
    headers = {
        "Authorization": "Bearer %s" % (bot_token.decode('utf-8'),),
        "Content-Type": "application/json; charset=utf-8",
    }
    resp = requests.post(url, json=msg, headers=headers)
    if resp.status_code != 200:
        raise Exception("Error calling slack api (%s): %s" % (resp.status_code, resp.content))
    return resp.json()

