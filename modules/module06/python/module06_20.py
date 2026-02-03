"""
Module 06: S3 オブジェクト取得（Resource API）

デモ内容:
- boto3.resource('s3') を使用したオブジェクト取得
- エラーハンドリングの実装例

実行方法:
  python3 module06_20.py

前提条件:
  - S3バケットが存在すること
  - 指定したオブジェクトキーが存在すること
"""
import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME
import boto3
import botocore

s3 = boto3.resource('s3')

def get_object(bucket, object_key):
    try:
        obj = s3.Object(bucket, object_key)
        body = obj.get()['Body'].read()
        print("Got object", object_key, "from bucket", bucket, ".")
    except botocore.exceptions.ClientError:
        print("Couldn't get object", object_key, "from bucket", bucket, ".")
    else:
        return body

if __name__ == "__main__":
    # オブジェクトキーは実際に存在するものを指定してください
    OBJECT_KEY = 'sample.txt'
    print(f"Getting object from bucket: {BUCKET_NAME}")
    body = get_object(BUCKET_NAME, OBJECT_KEY)
    if body:
        print(body)
