"""
Module 03: S3 オブジェクト一覧（Client API vs Resource API）

デモ内容:
- Client API (list_objects_v2) と Resource API (bucket.objects.all()) の比較
- 同じ操作を異なるAPIで実装する例

実行方法:
  python3 module03_16.py

前提条件:
  - S3バケットが存在すること（module05_28.py で作成）
  - バケット内にオブジェクトが存在すること
"""
import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME
import boto3

def listClient():
    s3client = boto3.client('s3')
    response = s3client.list_objects_v2(Bucket=BUCKET_NAME)
    for content in response['Contents']:
        print(content['Key'], content['LastModified'])

def listResource():
    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket(BUCKET_NAME)
    for object in bucket.objects.all():
        print(object.key, object.last_modified)

if __name__ == "__main__": 
    listClient()
    # listResource()
