# 署名付きURLを作る
s3 = boto3.client('s3')
url = s3.generate_presigned_url(
    ClientMethod = 'get_objrct',
    Params = {'Bucket' : 'secretweb000', 'Key' : 'special.pdf'},
    ExpiresIn = 48 * 60 * 60,
    HttpMethod = 'Get')

# userテーブルに登録する
usertable = dynamodb.Table("user")
usertable.put_item(
    Item={
        'id' : nextseq,
        'username' : username,
        'email' : email,
        'accepted_at' : decimal.Decimal(str(now)),
        'host' : host,
        'url' : url
    }
)