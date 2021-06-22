import json
import os

def lambda_handler(event, context):

    body = {'result' : 1}

    return {
        'statusCode' : 200,
        'headers' : {
            'access-control-allow-origin' : os.environ['s3endpoint'],
            'content-type' : 'application/json'
        },
        'body' : json.dumps(body)
    }