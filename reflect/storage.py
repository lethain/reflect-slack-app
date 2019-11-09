import random


def reflect(team_id, user_id, text):
    print("Reflected(%s, %s): %s" % (team_id, user_id, text))


def recall(team_id, user_id, text):
    "Recall reflections for (`team_id`, `user_id`) filtered by parameters in `text`"
    return ["I did something {}".format(x) for x in range(random.randint(3, 10))]
