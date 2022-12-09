from __future__ import print_function
#import json
import base64

import logging 


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

def handler(event, context):
    LOGGER.info('Event: %s', event)

    for record in event['Records']:
       #Kinesis data is base64 encoded so decode here
       payload=base64.b64decode(record["kinesis"]["data"])
       print("Decoded payload: " + str(payload))
