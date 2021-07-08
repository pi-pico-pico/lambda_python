import json
import boto3

# SQSのキューを取得
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=os.environ['mailsendqueue'])

#SNSトピックを取得
sns = boto3.resource('sns')
topic = sns.Topic('')