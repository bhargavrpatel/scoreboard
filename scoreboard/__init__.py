import logging
from collections import namedtuple

import json
import falcon


Intent = namedtuple('Intent', ['name', 'limit', 'first_player',
                               'second_player'])
logging.basicConfig(
    filename='/tmp/scoreboard_request_logs.log', level=logging.DEBUG,
    format="[%(asctime)s] [%(process)d] %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p')


def _create_intent(intent):
    name = intent['name']
    slots = {k: v.get('value') for k, v in intent['slots'].iteritems()}
    return Intent(
        name=name,
        limit=int(slots['limit'] or 11),
        first_player=slots['FirstPlayer'],
        second_player=slots['SecondPlayer']
    )


class AlexaResource:
    def on_post(self, req, resp):
        request_body = json.loads(req.stream.read())
        request_body = request_body['request']
        logging.info("Got an incoming request...")
        if request_body['type'] == 'IntentRequest':
            logging.info('Got an intent type request...')
            intent = _create_intent(request_body['intent'])
            msg = ('Starting a game between {} and {} for {} points'
                   .format(intent.first_player, intent.second_player,
                           intent.limit))
            logging.info('Returning with message: \'{}\''.format(msg))
            resp.status = falcon.HTTP_200
            resp.set_header('Content-Type', 'application/json')
            resp.body = json.dumps({
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": msg
                    }
                }
            })
            return resp
        resp.status = falcon.HTTP_400
        resp.set_header('Content-Type', 'application/json')
        resp.body = json.dumps({
            "version": "1.0",
            "response": {
                "error": "Service called with invalid parameters"
            }
        })


api = falcon.API()
api.add_route('/alexa', AlexaResource())
