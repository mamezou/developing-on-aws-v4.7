"""
DynamoDB GSI マルチ属性キー デモ - サンプルデータ投入

100件の注文データを投入します。
"""

import boto3
from datetime import datetime, timedelta
import random
import sys
sys.path.insert(0, '../../../../')
from config import REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)

TABLE_NAME = 'Orders-GSI-Demo'

CUSTOMERS = ['CUST-123', 'CUST-456', 'CUST-789']
STATUSES = ['pending', 'processing', 'completed', 'cancelled']
PRODUCTS = ['ノートPC', 'マウス', 'キーボード', 'モニター', 'ヘッドセット']


def main():
    print(f"テーブル: {TABLE_NAME}")
    print("100件のサンプルデータを投入します...\n")
    
    for i in range(100):
        order_date = (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
        
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'order_id': {'S': f'ORD-{i:04d}'},
                'customer_id': {'S': random.choice(CUSTOMERS)},
                'status': {'S': random.choice(STATUSES)},
                'order_date': {'S': order_date},
                'amount': {'N': str(random.randint(1000, 50000))},
                'product_name': {'S': random.choice(PRODUCTS)}
            }
        )
        
        if (i + 1) % 20 == 0:
            print(f"  {i + 1} / 100 完了")
    
    print("\n✅ サンプルデータ投入完了")


if __name__ == '__main__':
    main()
