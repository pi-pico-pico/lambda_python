import json
import boto3
import os

# SQSのキューを取得
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=os.environ['mailsendqueue'])

# SNSトピックを取得
sns = boto3.resource('sns')
# 下記修正
topic = sns.Topic('')

def lambda_handler(event, context):
    # キューの待ち数を確認する
    n = queue.attributes['ApproximateNumberOfMessages']
    # 10単位でSNSトピックに通知する
    for i in range(int(int((n + 9) / 10))):
        topic.publish(
            Message=os.environ['mailsendqueue']
        )