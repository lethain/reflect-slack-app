"""
Simple Slack application to track accomplishments.

See https://github.com/lethain/reflect-slack-app
    https://lethain.com/creating-reflect-slack-app/

"""
import os
from utils import verify
from api import oauth_access
from commands import reflect_command, recall_command
from events import url_verification_event, reaction_added_event, app_home_opened_event
from storage import set_credentials


ROUTES = (
    ('event/url_verification', url_verification_event),
    ('event/event_callback/app_home_opened', app_home_opened_event),
    ('event/event_callback/reaction_added', reaction_added_event),
    ('command/reflect', reflect_command),
    ('command/recall', recall_command),
)

def dispatch(request):
    signing_secret = os.environ['SLACK_SIGN_SECRET'].encode('utf-8')
    verify(request, signing_secret)

    # events are application/json, and
    # slash commands are sent as x-www-form-urlencoded
    route = "unknown"
    if request.content_type == 'application/json':
        parsed = request.json
        event_type = parsed['type']
        route = 'event/' + event_type
        if 'event' in parsed and 'type' in parsed['event']:
            route += '/' + parsed['event']['type']
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
        route = 'command/' + data['command'].strip('/')

    for path, handler in ROUTES:
        if path == route:
            return handler(request)

    print("couldn't handle route(%s), json(%s), form(%s)" % (route, request.json, request.form))
    raise Exception("couldn't handle route %s" % (route,))


def oauth_redirect(request):
    code = request.args.get('code')
    resp = oauth_access(code)
    team_id = resp['team_id']
    set_credentials(team_id, resp)
