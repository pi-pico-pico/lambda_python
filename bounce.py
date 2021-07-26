import json
import boto3

# リージョンが違うため、明示的に指定してる点に注意
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table('mailaddress')

def lambda_handler(event, context):
    for rec in event['Records']: