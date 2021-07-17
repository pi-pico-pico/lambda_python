import json
import boto3

sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mailaddress')

client = boto3.client('ses', region_name='us-east-1')
MAILFROM= ''


def lambda_handler(event, context):
    # 届いた通知を処理する
    for rec in event['Records']:
        snsmessage = rec['Sns']['Message']
        # SQSのキューを取得
        queue = sqs.get_queue_by_name(QueueName=snsmessage)
        # キューからメッセージを読み込む
        messages = queue.receive_messages(MessageAttributeNames=['All'], MaxNumberOfMessages = 10)

        # メッセージを処理してメールを送信する
        for m in messages:
            # キューの内容
            email = m.body
            if m.message_attributes is not None:
                print("Sending……")
                username = m.message_attributes.get('username').get('StringValue')
                backetname = m.message_attributes.get('backetname').get('StringValue')
                filename = m.message_attributes.get('filename').get('StringValue')
                
