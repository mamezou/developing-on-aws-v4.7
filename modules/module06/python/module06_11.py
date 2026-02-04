"""
Module 06: S3 バケット作成（Client API）

デモ内容:
- boto3.client('s3') を使用したバケット作成
- LocationConstraint によるリージョン指定
- 既存バケットの確認

実行方法:
  python3 module06_11.py
"""
import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME, REGION
import boto3
from botocore.exceptions import ClientError

def create_bucket():
    s3_client = boto3.client('s3', region_name=REGION)
    
    # 既存チェック
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f'✅ バケット {BUCKET_NAME} は既に存在します')
        return
    except ClientError:
        pass
    
    location = {'LocationConstraint': REGION}
    print(f'バケット {BUCKET_NAME} の作成をリクエストします')
    s3_client.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration=location)
    print('✅ バケットの作成が完了しました')

if __name__ == "__main__":
    print(f"リージョン: {REGION}")
    print(f"バケット名: {BUCKET_NAME}\n")
    create_bucket()
