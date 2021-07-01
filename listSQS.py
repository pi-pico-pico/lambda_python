import json
import urllib.parse
import boto3
from boto3.dynamodb.conditions import key, attr

def lambda_handler(event, context):
    # ①DynamoDBのmailaddressテーブルを操作するオブジェクト
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('mailaddress')

    # ②SQSのキューを操作するオブジェクト
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName="mailsendqueue000")
    
    for rec in event['Records']:
        # ③S3に置かれたファイルパスを取得
        backetname = rec['s3']['bucket']['name']
        filename = rec['s3']['object']['key']

        # ④haserrorが0のものをmailaddressテーブルから取得
        response = table.query(
            IndexName='haserror-index',
            KeyConditionExpression=Key('header').eq(0)
        )

        # ⑤上記の１件１件についてグループ処理
        for item in response['Item']:
            # ⑥送信済みを示すissendを0にする
            table.update_item(
                Key={'email' : item['email']},
                UpdateExpression="set issend=:val",
                MessageAttributeValues={
                    ':val' : 0
                }
            )
            # ⑦SQSにメッセージとして登録する
            spsresponse = queue.send_message(
                MessageBody=item['email'],
                MessageAttributes={
                    'username' : {
                        'DataType' : 'String',
                        'StringValue' : item['username']
                    },
                    'backetname' : {
                        'DataType' : 'String',
                        'StringValue' : backetname
                    },
                    'filename' : {
                        'DataType' : 'String',
                        'StringValue' : filename
                    }
                }
            )
            # 結果をログに出力しておく
            print(json.dumps(spsresponse))
