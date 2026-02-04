"""
Module 05: S3 バケット作成（Resource API）

デモ内容:
- boto3.resource('s3') を使用したバケット作成
- Resource API の高レベルな操作
- 既存バケットの確認

実行方法:
  python3 module05_28.py
"""
import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME, REGION
import boto3
from botocore.exceptions import ClientError

def create_bucket():
    """S3 バケットを作成（既存の場合はスキップ）"""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    
    # 既存チェック
    try:
        s3.meta.client.head_bucket(Bucket=BUCKET_NAME)
        print(f"✅ バケット {BUCKET_NAME} は既に存在します")
        return bucket
    except ClientError:
        pass  # バケットが存在しない
    
    # バケット作成
    print(f"バケットを作成: {BUCKET_NAME}")
    bucket.create(
        CreateBucketConfiguration={
            'LocationConstraint': REGION
        }
    )
    print(f"✅ バケット作成完了: {BUCKET_NAME}")
    
    return bucket

if __name__ == "__main__":
    print(f"リージョン: {REGION}")
    print(f"バケット名: {BUCKET_NAME}\n")
    create_bucket()
    
    print(f"\n削除する場合:")
    print(f"  aws s3 rb s3://{BUCKET_NAME} --force")
