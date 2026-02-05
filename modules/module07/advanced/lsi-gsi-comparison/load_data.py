"""
LSI vs GSI 比較デモ: サンプルデータ投入

ECサイトの注文データを投入します。
"""
import boto3
from myconfig import TABLE_NAME

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# サンプル注文データ
ORDERS = [
    # 田中さんの注文
    {'customer_id': 'tanaka', 'order_date': '2024-01-15', 'order_id': 'ORD001', 'product_id': 'LAPTOP01', 'status': 'delivered', 'amount': 150000},
    {'customer_id': 'tanaka', 'order_date': '2024-02-20', 'order_id': 'ORD002', 'product_id': 'MOUSE01', 'status': 'delivered', 'amount': 3000},
    {'customer_id': 'tanaka', 'order_date': '2024-03-10', 'order_id': 'ORD003', 'product_id': 'KEYBOARD01', 'status': 'shipped', 'amount': 15000},
    
    # 鈴木さんの注文
    {'customer_id': 'suzuki', 'order_date': '2024-01-20', 'order_id': 'ORD004', 'product_id': 'LAPTOP01', 'status': 'delivered', 'amount': 150000},
    {'customer_id': 'suzuki', 'order_date': '2024-02-25', 'order_id': 'ORD005', 'product_id': 'MONITOR01', 'status': 'delivered', 'amount': 45000},
    
    # 佐藤さんの注文
    {'customer_id': 'sato', 'order_date': '2024-02-01', 'order_id': 'ORD006', 'product_id': 'KEYBOARD01', 'status': 'delivered', 'amount': 15000},
    {'customer_id': 'sato', 'order_date': '2024-03-05', 'order_id': 'ORD007', 'product_id': 'LAPTOP01', 'status': 'processing', 'amount': 150000},
    {'customer_id': 'sato', 'order_date': '2024-03-15', 'order_id': 'ORD008', 'product_id': 'MOUSE01', 'status': 'processing', 'amount': 3000},
]

def load_data():
    print(f"=== サンプルデータ投入: {TABLE_NAME} ===\n")
    
    with table.batch_writer() as batch:
        for order in ORDERS:
            batch.put_item(Item=order)
            print(f"  {order['customer_id']}: {order['product_id']} ¥{order['amount']:,}")
    
    print(f"\n✅ {len(ORDERS)}件の注文データを投入しました")

if __name__ == "__main__":
    load_data()
    print(f"\n次のステップ: python3 query_demo.py")
