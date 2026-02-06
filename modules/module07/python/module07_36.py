"""
Module 07: DynamoDB テーブル作成（Client API）

デモ内容:
- boto3.client('dynamodb') を使用したテーブル作成
- Client API と Resource API の違いを理解する
- デモ終了時に自動クリーンアップ

実行方法:
  python3 module07_36.py
"""
import sys
import os

# スクリプトのディレクトリを基準にパスを解決（どこから実行しても動作）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '..', '..', '..'))
from config import STUDENT_ID
import boto3
import time

# デモ用テーブル名（タイムスタンプ付き）
DEMO_TABLE_NAME = f"demo-client-{STUDENT_ID}-{int(time.time())}"

def main():
    dynamodb = boto3.client('dynamodb')
    
    print(f"=== DynamoDB テーブル作成（Client API）===")
    print(f"テーブル名: {DEMO_TABLE_NAME}\n")
    
    # テーブル作成
    print("1. テーブルを作成...")
    dynamodb.create_table(
        TableName=DEMO_TABLE_NAME,
        AttributeDefinitions=[
            {'AttributeName': 'UserId', 'AttributeType': 'S'}
        ],
        KeySchema=[
            {'AttributeName': 'UserId', 'KeyType': 'HASH'}
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    print(f'   リクエスト送信完了')
    
    # Waiter で待機
    print("2. テーブル作成完了を待機...")
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=DEMO_TABLE_NAME)
    print("   ✅ 作成完了")
    
    # テーブル情報表示
    response = dynamodb.describe_table(TableName=DEMO_TABLE_NAME)
    print(f"\n3. テーブル情報:")
    print(f"   状態: {response['Table']['TableStatus']}")
    print(f"   ARN: {response['Table']['TableArn']}")
    
    # クリーンアップ
    print(f"\n4. クリーンアップ（テーブル削除）...")
    dynamodb.delete_table(TableName=DEMO_TABLE_NAME)
    waiter = dynamodb.get_waiter('table_not_exists')
    waiter.wait(TableName=DEMO_TABLE_NAME)
    print(f"   ✅ 削除完了")

if __name__ == "__main__":
    main()
