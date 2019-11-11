import os
import requests
from storage import get_credentials


def oauth_access(code):
    url = "https://slack.com/api/oauth.access"
    client_id = os.environ['SLACK_CLIENT_ID'].encode('utf-8')
    client_secret = os.environ['SLACK_CLIENT_SECRET'].encode('utf-8')
    data = {
        'code': code,
    }

    auth = (client_id, client_secret)
    resp = requests.post(url, data=data, auth=auth)
    return resp.json()


def get_message(team_id, channel, msg_ts):
    url = "https://slack.com/api/conversations.history"
    oauth_token = get_credentials(team_id)['oauth']
    params = {
        'token': oauth_token,
        'channel': channel,
        'latest': msg_ts,
        'limit': 1,
        'inclusive': True
    }
    resp = requests.get(url, params=params)
    return resp.json()


def slack_api(team_id, endpoint, msg):
    url = "https://slack.com/api/%s" % (endpoint,)
    bot_token = get_credentials(team_id)['bot']
    headers = {
        "Authorization": "Bearer %s" % (bot_token.decode('utf-8'),),
        "Content-Type": "application/json; charset=utf-8",
    }
    resp = requests.post(url, json=msg, headers=headers)
    if resp.status_code != 200:
        raise Exception("Error calling slack api (%s): %s" % (resp.status_code, resp.content))
    return resp.json()
