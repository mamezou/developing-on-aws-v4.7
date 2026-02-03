"""
Module 07: DynamoDB テーブル作成（Client API）

デモ内容:
- boto3.client('dynamodb') を使用したテーブル作成
- Client API と Resource API の違いを理解する

実行方法:
  python3 module07_36.py
"""
import sys
sys.path.insert(0, '../../../')
from config import TABLE_NAME
import boto3

dynamodb = boto3.client('dynamodb')
table = dynamodb.create_table(
    TableName=TABLE_NAME,
    AttributeDefinitions=[
        {
            'AttributeName': 'UserId',
            'AttributeType': 'S'
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'UserId',
            'KeyType': 'HASH'
        }
    ],
    BillingMode='PAY_PER_REQUEST',
)

print(f'テーブル {TABLE_NAME} の作成をリクエストしました')

# テーブルの削除
# dynamodb.delete_table(TableName=TABLE_NAME)

# テーブルの一覧表示
# aws dynamodb list-tables
