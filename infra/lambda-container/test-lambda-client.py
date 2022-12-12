import requests
import base64
import json

class Base64Encoder(json.JSONEncoder):
    # pylint: disable=method-hidden
    def default(self, o):
        if isinstance(o, bytes):
            return base64.b64encode(o).decode()
        if isinstance(o, dict):
            return base64.b64encode(o).encode('utf-8').decode()
        return json.JSONEncoder.default(self, o)

data = {
    "records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49590338271490256608559692538361571095921575989136588898",
                "data": b'{"name": "David", "age": 35}',
                "approximateArrivalTimestamp": 1545084650.987
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000006:49590338271490256608559692538361571095921575989136588898",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::123456789012:role/lambda-kinesis-role",
            "awsRegion": "us-east-2",
            "eventSourceARN": "arn:aws:kinesis:us-east-2:123456789012:stream/lambda-stream"
        }
    ]
}

url = 'http://localhost:9000/2015-03-31/functions/function/invocations'


message = json.dumps(data, cls=Base64Encoder)

# x = requests.post(url, data=data)

x = base64.b64encode(json.dumps({'name': "David"}).encode('utf-8'))
y = base64.b64decode(x)
print(json.loads(y))

x = requests.post(url, data=message)
