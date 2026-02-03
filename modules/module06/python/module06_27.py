"""
Module 06: S3 Presigned URL 生成

デモ内容:
- generate_presigned_url() を使用した署名付きURL生成
- 一時的なアクセス権限の付与

実行方法:
  python3 module06_27.py

前提条件:
  - S3バケットが存在すること
"""
import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME
import boto3

# オブジェクトキーは実際に存在するものを指定してください
OBJECT_KEY = 'sample.txt'

print(f"Generating presigned URL for: {BUCKET_NAME}/{OBJECT_KEY}")

url = boto3.client('s3').generate_presigned_url(
    ClientMethod='get_object',
    Params={ 'Bucket': BUCKET_NAME, 'Key': OBJECT_KEY },
    ExpiresIn=3600
)

print(f"Presigned URL (valid for 1 hour):")
print(url)
