"""
Module 03: DynamoDB テーブル作成（Resource API）

デモ内容:
- boto3.resource('dynamodb') を使用したテーブル作成
- Waiter を使用したテーブル作成完了の待機

実行方法:
  python3 module03_26.py
"""
import sys
sys.path.insert(0, '../../../')
from config import TABLE_NAME
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
    TableName=TABLE_NAME,
    AttributeDefinitions=[
        {
            'AttributeName': 'pk',
            'AttributeType': 'S'
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'pk',
            'KeyType': 'HASH'
        }
    ],
    BillingMode='PAY_PER_REQUEST',
)

print(f'テーブル {TABLE_NAME} の作成をリクエストしました。')
table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
print('テーブルの作成が完了しました。')

print(table.item_count)

# CLI:テーブルの削除
# aws dynamodb delete-table --table-name Notes
