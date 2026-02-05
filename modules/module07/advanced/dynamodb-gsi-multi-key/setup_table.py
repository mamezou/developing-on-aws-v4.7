"""
DynamoDB GSI マルチ属性キー デモ - テーブル作成

Python スクリプトでテーブルを作成します。
"""

import boto3
from botocore.exceptions import ClientError
from myconfig import TABLE_NAME, INDEX_NAME, REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)


def create_table():
    print(f"テーブル作成: {TABLE_NAME}")
    
    try:
        dynamodb.create_table(
            TableName=TABLE_NAME,
            BillingMode='PAY_PER_REQUEST',
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'customer_id', 'AttributeType': 'S'},
                {'AttributeName': 'status', 'AttributeType': 'S'},
            ],
            KeySchema=[
                {'AttributeName': 'order_id', 'KeyType': 'HASH'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': INDEX_NAME,
                    'KeySchema': [
                        {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'status', 'KeyType': 'RANGE'},
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                },
            ],
        )
        
        # テーブルがアクティブになるまで待機
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=TABLE_NAME)
        
        print(f"✅ テーブル作成完了: {TABLE_NAME}")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"⚠️ テーブルは既に存在します: {TABLE_NAME}")
        else:
            raise


if __name__ == '__main__':
    create_table()
