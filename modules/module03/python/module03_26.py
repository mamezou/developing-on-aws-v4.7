"""
Module 03: DynamoDB テーブル作成（Resource API）

デモ内容:
- boto3.resource('dynamodb') を使用したテーブル作成
- Waiter を使用したテーブル作成完了の待機
- デモ終了時に自動クリーンアップ

実行方法:
  python3 module03_26.py
"""
import sys
sys.path.insert(0, '../../../')
from config import STUDENT_ID
import boto3
import time

# デモ用テーブル名（タイムスタンプ付きで一意性確保）
DEMO_TABLE_NAME = f"demo-table-{STUDENT_ID}-{int(time.time())}"

def main():
    dynamodb = boto3.resource('dynamodb')
    
    print(f"=== DynamoDB テーブル作成デモ ===")
    print(f"テーブル名: {DEMO_TABLE_NAME}\n")
    
    # テーブル作成
    print("1. テーブルを作成...")
    table = dynamodb.create_table(
        TableName=DEMO_TABLE_NAME,
        AttributeDefinitions=[
            {'AttributeName': 'pk', 'AttributeType': 'S'}
        ],
        KeySchema=[
            {'AttributeName': 'pk', 'KeyType': 'HASH'}
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    print(f"   リクエスト送信完了")
    
    # Waiter で待機
    print("2. Waiter でテーブル作成完了を待機...")
    start = time.time()
    table.meta.client.get_waiter('table_exists').wait(TableName=DEMO_TABLE_NAME)
    elapsed = time.time() - start
    print(f"   ✅ 作成完了（{elapsed:.1f}秒）")
    
    # テーブル情報表示
    table.reload()
    print(f"\n3. テーブル情報:")
    print(f"   状態: {table.table_status}")
    print(f"   ARN: {table.table_arn}")
    
    # クリーンアップ
    print(f"\n4. クリーンアップ（テーブル削除）...")
    table.delete()
    table.meta.client.get_waiter('table_not_exists').wait(TableName=DEMO_TABLE_NAME)
    print(f"   ✅ 削除完了")

if __name__ == "__main__":
    main()
