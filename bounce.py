import json
import boto3

# リージョンが違うため、明示的に指定してる点に注意
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table('mailaddress')

def lambda_handler(event, context):
    for rec in event['Records']:
        # バウンスしたメールアドレスの取得
        message = rec['Sns']['Message']
        data = json.loads(message)
        bounces = data['bounce']['bounceRecipients']
        for b in bounces:
            email = b['emailAddress']
            # haserrorを1に設定する
            response = table.update_item(
                Key={'email' : email},
                UpdateExpressionAttributeValues= {
                    ':val' : 1
                }
            )