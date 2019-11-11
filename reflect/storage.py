import datetime
from google.cloud import firestore


DB = firestore.Client()


def credentials(team_id):
    return DB.collection('creds').document(team_id)


def set_credentials(team_id, data):
    creds = credentials(team_id)
    creds.set(data)

def get_credentials(team_id):
    creds = credentials(team_id).get().to_dict()
    return {
        'oauth': creds['access_token'],
        'bot': creds['bot']['bot_access_token'],
x    }


def tasks(team_id, user_id):
    key = "%s:%s" % (team_id, user_id)
    ref = DB.collection('users').document(key).collection('tasks')
    return ref


def reflect(team_id, user_id, text):
    doc = {
        'team': team_id,
        'user': user_id,
        'text': text,
        'ts': datetime.datetime.now(),
    }
    col = tasks(team_id, user_id)
    col.add(doc)


def recall(team_id, user_id, text):
    col = tasks(team_id, user_id)
    for task in col.stream():
        yield task.to_dict()['text']
