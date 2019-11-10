import datetime
from google.cloud import firestore


DB = firestore.Client()


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
