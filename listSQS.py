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
    