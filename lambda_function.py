import boto3
import pyminizip
import tempfile
import os


def lambda_handler(event, context):

    s3 = boto3.resource('s3')

    for rec in event['Records']:
        
        # ファイル名取得
        filename = rec['s3']['object']['key']

        # バケット名取得
        obj = s3.Object(rec['s3']['bucket']['name'], filename)

        # 詳細情報取得
        response = obj.get()

        # 一時ディレクトリ作成
        tmpdir = tempfile.TemporaryDirectory()
        fp = open(tmpdir.name + '/' + filename, 'wb')
        fp.write()
        fp.close()

        # 暗号化
        zipname = tempfile.mkstemp(suffix='.zip')[1]
        os.chdir(tmpdir.name)
        pyminizip.compress(filename, '', zipname, 'mypassword', 0)

        # S3にアップロード
        obj = s3.Object('examplebucketwrite', filename + '.zip')
        response = obj.put(
            Body = open(zipname, 'rb')
        )

        # 一時ファイルの削除
        tmpdir.cleanup()
        os.unlink(zipname)


# =================================
# =================================
# テストデータ作成
# =================================
# =================================
import json
if __name__ == "__main__":
    data = '''
    '''

    event = json.loads(data)
    context = None
    lambda_handler(event, context)