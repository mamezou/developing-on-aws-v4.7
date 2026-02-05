"""
LSI vs GSI 比較デモ: テーブル作成

LSIとGSI付きのOrdersテーブルを作成します。
"""
import boto3
from myconfig import TABLE_NAME, LSI_NAME, GSI_NAME

dynamodb = boto3.client('dynamodb')

def create_table():
    """LSIとGSI付きテーブルを作成"""
    print(f"=== テーブル作成: {TABLE_NAME} ===\n")
    
    # 既存テーブルチェック
    try:
        dynamodb.describe_table(TableName=TABLE_NAME)
        print(f"テーブル {TABLE_NAME} は既に存在します")
        print("削除する場合: python3 cleanup.py")
        return
    except dynamodb.exceptions.ResourceNotFoundException:
        pass
    
    print("テーブルを作成中...")
    print("  PK: customer_id, SK: order_date")
    print(f"  LSI ({LSI_NAME}): customer_id + amount")
    print(f"  GSI ({GSI_NAME}): product_id + order_date\n")
    
    dynamodb.create_table(
        TableName=TABLE_NAME,
        AttributeDefinitions=[
            {'AttributeName': 'customer_id', 'AttributeType': 'S'},
            {'AttributeName': 'order_date', 'AttributeType': 'S'},
            {'AttributeName': 'amount', 'AttributeType': 'N'},
            {'AttributeName': 'product_id', 'AttributeType': 'S'},
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
        GlobalSecondaryIndexes=[
            {
                'IndexName': GSI_NAME,
                'KeySchema': [
                    {'AttributeName': 'product_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'order_date', 'KeyType': 'RANGE'},
                ],
                'Projection': {'ProjectionType': 'ALL'}
            }
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    
    # 待機
    print("作成完了を待機中...")
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=TABLE_NAME)
    print("✅ テーブル作成完了\n")
    
    print("【LSI vs GSI の違い】")
    print("  LSI: テーブル作成時にのみ定義可能、後から追加不可")
    print("  GSI: テーブル作成後でも追加・削除可能")

if __name__ == "__main__":
    create_table()
    print(f"\n次のステップ: python3 load_data.py")
