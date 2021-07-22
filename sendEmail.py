import json
import boto3
import os

sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mailaddress')

client = boto3.client('ses', region_name='ap-northeast-1')
MAILFROM= os.environ['email']


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
                print(backetname)
                print(filename)
                print(username)
                print(email)

                # S3バケットから本文を取得する
                obj = s3.Object(backetname, filename)
                response = obj.get()
                maildata = response['Body'].read().decode('utf-8')
                datas = maildata.split("\n", 3)
                subject = datas[0]
                body = datas[2]

                # 送信済みでないことを確認し、また、送信済みに設定する
                response = table.update_item(
                    Key = {
                        'email' : email
                    },
                    UpdateExpression = "set issend=:val",
                    ExpressionAttributeValues = {
                    ':val' : 1
                    },
                    returnValues = 'UPDATED_OLD'
                )

                if response['Attributes']['issend'] == 0:
                    # メール送信
                    response = client.send_email(
                        Source=MAILFROM,
                        ReplyToAddresses=[MAILFROM],
                        Destination= {
                            'ToAddresses' : [
                                email
                            ]
                        },
                        Message={
                            'Subject': {
                                'Data' : subject,
                                'Charsest' : 'UTF-8'
                            },
                            'Body' : {
                                'Text' : {
                                    'Data' : body,
                                    'Charset' : 'UTF-8'
                            }
                        }
                    }
                )
                else:
                    print("Resend Skip")

                print("Send To" + email)
            else:
                print("Message None")

            # キューから取り除く
            m.delete()

