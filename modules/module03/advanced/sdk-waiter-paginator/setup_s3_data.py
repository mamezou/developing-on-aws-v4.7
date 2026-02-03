"""
S3 ダミーデータ作成スクリプト

Paginator デモ用に 1500 個のダミーファイルを S3 に作成します。
"""

import boto3
import sys
sys.path.insert(0, '../../../../')
from config import BUCKET_NAME, REGION

s3_client = boto3.client('s3', region_name=REGION)

def create_bucket_if_not_exists():
    """バケットが存在しない場合は作成"""
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f"バケット {BUCKET_NAME} は既に存在します")
    except:
        print(f"バケット {BUCKET_NAME} を作成します...")
        s3_client.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
        print("✅ バケット作成完了")


def create_dummy_files(count=1500):
    """ダミーファイルを作成"""
    print(f"\n{count} 個のダミーファイルを作成します...")
    
    for i in range(count):
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f'paginator-demo/file_{i:04d}.txt',
            Body=f'This is dummy file {i}'
        )
        if (i + 1) % 100 == 0:
            print(f"  {i + 1} / {count} 完了")
    
    print(f"✅ {count} 個のダミーファイル作成完了")


def main():
    create_bucket_if_not_exists()
    create_dummy_files()
    print(f"\nバケット: {BUCKET_NAME}")
    print("プレフィックス: paginator-demo/")


if __name__ == '__main__':
    main()
