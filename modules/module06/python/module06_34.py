"""
Module 06: S3 Paginator によるオブジェクト一覧

デモ内容:
- Paginator を使用した大量オブジェクトの効率的な取得
- ページネーション処理の自動化

実行方法:
  python3 module06_34.py

前提条件:
  - S3バケットが存在すること
"""
import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME
import boto3

client = boto3.client('s3')

print(f"Listing objects in bucket: {BUCKET_NAME}")

paginator = client.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(
    Bucket=BUCKET_NAME,
    PaginationConfig={'MaxItems': 3000}
)

for page in page_iterator:
    if 'Contents' in page:
        for obj in page['Contents']:
            print(f"  {obj['Key']}")
    else:
        print("  (no objects found)")
