"""
Module 03: Client API vs Resource API の比較

デモ内容:
- 同じ S3 操作を Client API と Resource API で実装
- コード量、戻り値の型、使い勝手の違いを比較

実行方法:
  python3 module03_16.py

前提条件:
  - S3バケットが存在すること
  - バケット作成: python3 ../../module05/python/module05_28.py
"""
import sys
import os

# スクリプトのディレクトリを基準にパスを解決（どこから実行しても動作）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '..', '..', '..'))
from config import BUCKET_NAME
import boto3
from botocore.exceptions import ClientError

def demo_client_api():
    """
    Client API: 低レベル、AWS API に近い
    - 戻り値は dict（JSON形式）
    - ページネーションは手動
    - 細かい制御が可能
    """
    print("=" * 50)
    print("【Client API】boto3.client('s3')")
    print("=" * 50)
    
    s3 = boto3.client('s3')
    
    # バケット一覧
    print("\n▼ バケット一覧取得")
    print("  コード: s3.list_buckets()")
    response = s3.list_buckets()
    print(f"  戻り値の型: {type(response)}")  # dict
    print(f"  バケット数: {len(response['Buckets'])}")
    
    # オブジェクト一覧
    print("\n▼ オブジェクト一覧取得")
    print(f"  コード: s3.list_objects_v2(Bucket='{BUCKET_NAME}')")
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        print(f"  戻り値の型: {type(response)}")  # dict
        if 'Contents' in response:
            print(f"  オブジェクト数: {len(response['Contents'])}")
            for obj in response['Contents'][:3]:
                print(f"    - {obj['Key']} (型: dict)")
        else:
            print("  オブジェクトなし")
    except ClientError as e:
        print(f"  ❌ エラー: {e.response['Error']['Code']}")


def demo_resource_api():
    """
    Resource API: 高レベル、オブジェクト指向
    - 戻り値はオブジェクト（属性でアクセス）
    - イテレータで自動ページネーション
    - 直感的で書きやすい
    """
    print("\n" + "=" * 50)
    print("【Resource API】boto3.resource('s3')")
    print("=" * 50)
    
    s3 = boto3.resource('s3')
    
    # バケット一覧
    print("\n▼ バケット一覧取得")
    print("  コード: s3.buckets.all()")
    buckets = list(s3.buckets.all())
    print(f"  戻り値の型: {type(buckets[0]) if buckets else 'N/A'}")  # s3.Bucket
    print(f"  バケット数: {len(buckets)}")
    
    # オブジェクト一覧
    print("\n▼ オブジェクト一覧取得")
    print(f"  コード: s3.Bucket('{BUCKET_NAME}').objects.all()")
    try:
        bucket = s3.Bucket(BUCKET_NAME)
        objects = list(bucket.objects.all())
        if objects:
            print(f"  戻り値の型: {type(objects[0])}")  # s3.ObjectSummary
            print(f"  オブジェクト数: {len(objects)}")
            for obj in objects[:3]:
                print(f"    - {obj.key} (型: s3.ObjectSummary)")
        else:
            print("  オブジェクトなし")
    except ClientError as e:
        print(f"  ❌ エラー: {e.response['Error']['Code']}")


def show_comparison():
    """API の違いをまとめて表示"""
    print("\n" + "=" * 50)
    print("【比較まとめ】")
    print("=" * 50)
    print("""
┌─────────────┬──────────────────┬──────────────────┐
│   観点      │   Client API     │   Resource API   │
├─────────────┼──────────────────┼──────────────────┤
│ 抽象度      │ 低（AWS API直接）│ 高（OOP）        │
│ 戻り値      │ dict             │ オブジェクト     │
│ ページング  │ 手動             │ 自動             │
│ コード量    │ 多め             │ 少なめ           │
│ 細かい制御  │ ◎               │ △               │
│ 学習コスト  │ 低               │ 中               │
└─────────────┴──────────────────┴──────────────────┘

【使い分けの目安】
- Client API: 細かい制御が必要、パフォーマンス重視
- Resource API: 素早く実装、可読性重視
""")


if __name__ == "__main__":
    print(f"バケット: {BUCKET_NAME}\n")
    demo_client_api()
    demo_resource_api()
    show_comparison()
