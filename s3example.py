import boto3
import pyminizip
import tempfile
import os

filename = 'test.jpg'
s3 = boto3.resource('s3')

# ファイルの読み込み
obj = s3.Object('examplebucketread',filename)
response = obj.get()
tmpdir = tempfile.TemporaryDirectory()
fp = open(tmpdir.name + '/' + filename, 'wb')
fp.write(response['Body'].read)
fp.close()

# 暗号化
zipname = tempfile.mkstemp(sufix='.zip')[1]
os.chdir(tmpdir.name)
pyminizip.compress(filename, zipname, 'mypassword', 0)

# S3にアップロード
obj = s3.Object('examplebucketwrite', filename + '.zip')
response = obj.put(
    Body = open(zipname, 'rb')
)

tmpdir.cleanup()
os.unlink(zipname)


