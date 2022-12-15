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
        payload=base64.b64decode(record["data"])
        data = json.loads(payload)

        LOGGER.info('data: %s', data)
        # print("name is {} and he is {} years old" 
        #         .format(data["name"], data["age"]))

        out = {
            "name": data["name"],
            "age": data["age"]
        }

        # https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html
        output.append({
            'recordId': record["recordId"],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(out).encode('utf-8')).decode('utf-8')
        })

    LOGGER.info('Successfully processed {} records'.format(len(output)))
    return {'records': output}