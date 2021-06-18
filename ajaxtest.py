import json

body = {'result' : 1}

result = {
    'statusCode' : 200,
    'headers' : {
        'content-type' : 'application/json'
    },
    'body' : json.dumps(body)
}