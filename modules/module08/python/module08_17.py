"""
Module 08: DynamoDB テーブル作成 + Waiter（Client API）

デモ内容:
- boto3.client('dynamodb') を使用したテーブル作成
- Waiter を使用したテーブル作成完了の待機
- デモ終了時に自動クリーンアップ

実行方法:
  python3 module08_17.py
"""
import sys
sys.path.insert(0, '../../../')
from config import STUDENT_ID
import boto3
import time

# デモ用テーブル名（タイムスタンプ付き）
DEMO_TABLE_NAME = f"demo-waiter-{STUDENT_ID}-{int(time.time())}"

def main():
    dynamodb = boto3.client('dynamodb')
    
    print(f"=== DynamoDB Waiter デモ ===")
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
    
    # Waiter で待機（時間計測）
    print("2. Waiter でテーブル作成完了を待機...")
    start = time.time()
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=DEMO_TABLE_NAME)
    elapsed = time.time() - start
    print(f'   ✅ 作成完了（{elapsed:.1f}秒）')
    
    # クリーンアップ
    print(f"\n3. クリーンアップ（テーブル削除）...")
    dynamodb.delete_table(TableName=DEMO_TABLE_NAME)
    waiter = dynamodb.get_waiter('table_not_exists')
    waiter.wait(TableName=DEMO_TABLE_NAME)
    print(f"   ✅ 削除完了")

if __name__ == "__main__":
    main()
