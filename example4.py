import json

# イベント引数をログに書き出すプログラム
def lambda_handler(event, context):
    print(json.json.dumps(event, indent=4))
    
    # JSON形式の戻り値を設定する
    return {
        'statusCode' : 200,
        'headers' : {
            'content-type' : 'text/html'
        },
        'body' : '<html><body>OK</body></html>'
    }

