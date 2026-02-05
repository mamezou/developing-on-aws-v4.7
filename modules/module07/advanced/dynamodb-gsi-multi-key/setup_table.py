"""
DynamoDB GSI マルチ属性キー デモ - テーブル作成

従来方式（合成キー）とマルチ属性キー方式の2つのテーブルを作成します。
"""

import boto3
from botocore.exceptions import ClientError
from myconfig import TABLE_TRADITIONAL, TABLE_MULTI_ATTR, INDEX_NAME, REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)


def create_traditional_table():
    """従来方式: 合成キーを使った GSI"""
    print(f"\n📦 従来方式テーブル作成: {TABLE_TRADITIONAL}")
    print("   GSI: customer_id (PK) + composite_sk (SK)")
    print("   composite_sk = status#order_date#order_id")
    
    try:
        dynamodb.create_table(
            TableName=TABLE_TRADITIONAL,
            BillingMode='PAY_PER_REQUEST',
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'customer_id', 'AttributeType': 'S'},
                {'AttributeName': 'composite_sk', 'AttributeType': 'S'},  # 合成キー
            ],
            KeySchema=[
                {'AttributeName': 'order_id', 'KeyType': 'HASH'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': INDEX_NAME,
                    'KeySchema': [
                        {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'composite_sk', 'KeyType': 'RANGE'},  # 合成キー
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                },
            ],
        )
        
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=TABLE_TRADITIONAL)
        print(f"   ✅ 作成完了")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"   ⚠️ 既に存在します")
        else:
            raise


def create_multi_attr_table():
    """マルチ属性キー方式: 複数属性を直接指定"""
    print(f"\n🚀 マルチ属性キー方式テーブル作成: {TABLE_MULTI_ATTR}")
    print("   GSI: customer_id (PK) + [status, order_date, order_id] (SK)")
    print("   合成キー不要！")
    
    try:
        dynamodb.create_table(
            TableName=TABLE_MULTI_ATTR,
            BillingMode='PAY_PER_REQUEST',
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'customer_id', 'AttributeType': 'S'},
                {'AttributeName': 'status', 'AttributeType': 'S'},
                {'AttributeName': 'order_date', 'AttributeType': 'S'},
            ],
            KeySchema=[
                {'AttributeName': 'order_id', 'KeyType': 'HASH'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': INDEX_NAME,
                    'KeySchema': [
                        {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
                        # マルチ属性ソートキー: 3つの属性を指定
                        {'AttributeName': 'status', 'KeyType': 'RANGE'},
                        {'AttributeName': 'order_date', 'KeyType': 'RANGE'},
                        {'AttributeName': 'order_id', 'KeyType': 'RANGE'},
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                },
            ],
        )
        
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=TABLE_MULTI_ATTR)
        print(f"   ✅ 作成完了")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"   ⚠️ 既に存在します")
        else:
            raise


def main():
    print("=" * 60)
    print("DynamoDB GSI マルチ属性キー デモ - テーブル作成")
    print("=" * 60)
    
    create_traditional_table()
    create_multi_attr_table()
    
    print("\n" + "=" * 60)
    print("テーブル作成完了！次は setup_data.py を実行してください。")
    print("=" * 60)


if __name__ == '__main__':
    main()
