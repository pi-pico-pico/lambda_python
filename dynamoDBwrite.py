import json
import boto3
import urllib.parse
import time
import decimal

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

# 連番を更新して返す関数
def next_seq(table,tablename):
    response = table.update_item(
        Key={
            'tablename' : tablename
        },
        UpdateExpression="set seq = seq + :val",
        ExpressionAttributeValues= {
            ':val' : 1
        },
        ReturnValues='UPDATED_NEW'
    )
    return response['Attributes']['seq']

def lambda_handler(event, context):
    try:
        # シーケンスデータを得る
        seqtable = dtnamodb.Table('sequence')
        nextseq = next_seq(seqtable, 'user')

        # フォームに入力されたデータを得る
        param = urllib.parse.parse_qs(event['body'])
        username = param['username'][0]
        email = param['email'][0]

        # クライアントのIPを得る
        host = event['requestContext']['identity']['sourceIp']

        # 現在のUNIXタイムスタンプを得る
        now = time.time()

        # userテーブルに登録する
        usertable = dynamodb.Table("user")
        usertable.put_item(
            Item={
                'id' : nextseq,
                'username' : username,
                'email' : email,
                'accepted_at' : decimal.Decimal(str(now)),
                'host' : host
            }
        )

        # 結果を返す
        return {
            'statusCode' : 200,
            'headers' : {
                'content-type' : 'text/html'
            },
            'body' : '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>登録ありがとうございました。</body></html>'
        }

    except:
        import traceback
        traceback.print_exc()
        return {
                        'statusCode' : 500,
            'headers' : {
                'content-type' : 'text/html'
            },
            'body' : '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>内部エラーが発生しました。</body></html>'
        }

        