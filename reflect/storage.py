from google.cloud import firestore
import datetime


TASK_COLLECTION = 'tasks'

db = firestore.Client()


def tasks(team_id, user_id):
    key = "%s:%s" % (team_id, user_id)
    ref = db.collection('users').document(key).collection('tasks')
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
    "Recall reflections for (`team_id`, `user_id`) filtered by parameters in `text`"
    return ["I did something {}".format(x) for x in range(random.randint(3, 10))]
