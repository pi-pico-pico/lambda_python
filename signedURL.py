# 署名付きURLを作る
s3 = boto3.client('s3')
url = s3.generate_presigned_url(
    ClientMethod = 'get_objrct'
    Params = {'Bucket' : 'secretweb000', 'Key' : 'special.pdf'},
    ExpiresIn = 48 * 60 * 60,
    HttpMethod = 'Get')

# userテーブルに登録する