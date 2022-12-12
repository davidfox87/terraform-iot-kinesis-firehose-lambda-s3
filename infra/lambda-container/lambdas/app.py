from __future__ import print_function
import json
import base64

import logging 


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

def handler(event, context):

    LOGGER.info('Event: %s', event)
    
    output = []
    for record in event['records']:
        LOGGER.info('record: %s', record)
        
        #Kinesis data is base64 encoded so decode here
        payload=base64.b64decode(record["kinesis"]["data"])
        data = json.loads(payload)

        print("name is {} and he is {} years old" 
                .format(data['name'], data['age']))

    LOGGER.info('Successfully processed {} records'.format(len(event['records'])))
    return {'records': output}