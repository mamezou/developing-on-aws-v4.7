"""
Module 06: S3 バケット作成（Client API）

デモ内容:
- boto3.client('s3') を使用したバケット作成
- LocationConstraint によるリージョン指定

実行方法:
  python3 module06_11.py
"""
import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME, REGION
import boto3

s3_client = boto3.client('s3', region_name=REGION)
location = { 'LocationConstraint': REGION }

print(f'バケット {BUCKET_NAME} の作成をリクエストします')
s3_client.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration=location)
print('バケットの作成が完了しました')

# バケットの削除
# s3_client.delete_bucket(Bucket=BUCKET_NAME)
