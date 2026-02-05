"""
DynamoDB GSI マルチ属性キー デモ - サンプルデータ投入

両方のテーブルに同じデータを投入します。
従来方式では合成キーを作成、マルチ属性キー方式ではそのまま保存。
"""

import boto3
from datetime import datetime, timedelta
import random
from myconfig import TABLE_TRADITIONAL, TABLE_MULTI_ATTR, REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)

CUSTOMERS = ['CUST-001', 'CUST-002', 'CUST-003']
STATUSES = ['pending', 'processing', 'completed', 'cancelled']
PRODUCTS = ['ノートPC', 'マウス', 'キーボード', 'モニター', 'ヘッドセット']


def put_traditional_item(item_data):
    """従来方式: 合成キーを作成して保存"""
    # 合成キーを手動で作成（面倒！）
    composite_sk = f"{item_data['status']}#{item_data['order_date']}#{item_data['order_id']}"
    
    dynamodb.put_item(
        TableName=TABLE_TRADITIONAL,
        Item={
            'order_id': {'S': item_data['order_id']},
            'customer_id': {'S': item_data['customer_id']},
            'status': {'S': item_data['status']},
            'order_date': {'S': item_data['order_date']},
            'amount': {'N': str(item_data['amount'])},
            'product_name': {'S': item_data['product_name']},
            # 合成キー（GSI 用）
            'composite_sk': {'S': composite_sk},
        }
    )


def put_multi_attr_item(item_data):
    """マルチ属性キー方式: そのまま保存（合成キー不要！）"""
    dynamodb.put_item(
        TableName=TABLE_MULTI_ATTR,
        Item={
            'order_id': {'S': item_data['order_id']},
            'customer_id': {'S': item_data['customer_id']},
            'status': {'S': item_data['status']},
            'order_date': {'S': item_data['order_date']},
            'amount': {'N': str(item_data['amount'])},
            'product_name': {'S': item_data['product_name']},
            # 合成キー不要！
        }
    )


def main():
    print("=" * 60)
    print("DynamoDB GSI マルチ属性キー デモ - データ投入")
    print("=" * 60)
    
    print(f"\n50件のサンプルデータを両テーブルに投入します...")
    print(f"  - {TABLE_TRADITIONAL} (従来方式)")
    print(f"  - {TABLE_MULTI_ATTR} (マルチ属性キー方式)")
    
    for i in range(50):
        order_date = (datetime.now() - timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d')
        
        item_data = {
            'order_id': f'ORD-{i:04d}',
            'customer_id': random.choice(CUSTOMERS),
            'status': random.choice(STATUSES),
            'order_date': order_date,
            'amount': random.randint(1000, 50000),
            'product_name': random.choice(PRODUCTS),
        }
        
        put_traditional_item(item_data)
        put_multi_attr_item(item_data)
        
        if (i + 1) % 10 == 0:
            print(f"  {i + 1} / 50 完了")
    
    print("\n" + "=" * 60)
    print("✅ データ投入完了！次は query_demo.py を実行してください。")
    print("=" * 60)
    
    print("\n【ポイント】")
    print("従来方式では put_traditional_item() で合成キーを作成しています。")
    print("マルチ属性キー方式では put_multi_attr_item() でそのまま保存しています。")
    print("コードを比較してみてください！")


if __name__ == '__main__':
    main()
