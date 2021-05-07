# S3にアップロードされたファイル名の取得
def lambda_handler(event, context):
    
    for rec in event['Records']:
        print ([rec['s3']['object']['key']])

