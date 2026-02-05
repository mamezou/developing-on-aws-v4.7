"""
LSI vs GSI 比較デモ: テーブル作成

LSI付きのOrdersテーブルを作成し、後からGSIを追加します。
これにより「LSIはテーブル作成時のみ」「GSIは後から追加可能」を体験できます。
"""
import boto3
import time
from myconfig import TABLE_NAME, LSI_NAME, GSI_NAME

dynamodb = boto3.client('dynamodb')

def create_table_with_lsi():
    """LSI付きテーブルを作成"""
    print(f"=== テーブル作成: {TABLE_NAME} ===\n")
    
    # 既存テーブルチェック
    try:
        dynamodb.describe_table(TableName=TABLE_NAME)
        print(f"テーブル {TABLE_NAME} は既に存在します")
        return
    except dynamodb.exceptions.ResourceNotFoundException:
        pass
    
    print("1. LSI付きテーブルを作成...")
    print("   PK: customer_id, SK: order_date")
    print(f"   LSI ({LSI_NAME}): customer_id + amount")
    
    dynamodb.create_table(
        TableName=TABLE_NAME,
        AttributeDefinitions=[
            {'AttributeName': 'customer_id', 'AttributeType': 'S'},
            {'AttributeName': 'order_date', 'AttributeType': 'S'},
            {'AttributeName': 'amount', 'AttributeType': 'N'},
            # product_id は GSI 追加時に定義する
        ],
        KeySchema=[
            {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
            {'AttributeName': 'order_date', 'KeyType': 'RANGE'},
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': LSI_NAME,
                'KeySchema': [
                    {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'amount', 'KeyType': 'RANGE'},
                ],
                'Projection': {'ProjectionType': 'ALL'}
            }
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    
    # 待機
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=TABLE_NAME)
    print("   ✅ テーブル作成完了\n")
    
    # GSIを後から追加
    add_gsi()

def add_gsi():
    """GSIを後から追加（LSIとの違いを体験）"""
    print("2. GSIを後から追加...")
    print(f"   GSI ({GSI_NAME}): product_id + order_date")
    print("   ※ LSIと違い、テーブル作成後でも追加できます\n")
    
    dynamodb.update_table(
        TableName=TABLE_NAME,
        AttributeDefinitions=[
            {'AttributeName': 'product_id', 'AttributeType': 'S'},
            {'AttributeName': 'order_date', 'AttributeType': 'S'},
        ],
        GlobalSecondaryIndexUpdates=[
            {
                'Create': {
                    'IndexName': GSI_NAME,
                    'KeySchema': [
                        {'AttributeName': 'product_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'order_date', 'KeyType': 'RANGE'},
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            }
        ]
    )
    
    # GSI作成完了を待機
    print("   GSI作成中（数十秒かかります）...")
    while True:
        response = dynamodb.describe_table(TableName=TABLE_NAME)
        gsi_list = response['Table'].get('GlobalSecondaryIndexes', [])
        if gsi_list and gsi_list[0]['IndexStatus'] == 'ACTIVE':
            break
        time.sleep(5)
        print("   .", end='', flush=True)
    
    print("\n   ✅ GSI作成完了")

if __name__ == "__main__":
    create_table_with_lsi()
    print(f"\n次のステップ: python load_data.py")
