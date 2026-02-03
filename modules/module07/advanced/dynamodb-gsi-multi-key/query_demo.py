"""
DynamoDB GSI マルチ属性キー デモ - クエリ実行

GSI を使用して複合条件でクエリを実行します。
"""

import boto3
from myconfig import TABLE_NAME, INDEX_NAME, REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)

CUSTOMER_ID = 'CUST-123'


def query_by_status():
    """クエリ1: ステータスのみ"""
    print("=== クエリ1: pending の注文 ===")
    
    response = dynamodb.query(
        TableName=TABLE_NAME,
        IndexName=INDEX_NAME,
        KeyConditionExpression='customer_id = :cid AND #status = :status',
        ExpressionAttributeNames={
            '#status': 'status'  # status は予約語
        },
        ExpressionAttributeValues={
            ':cid': {'S': CUSTOMER_ID},
            ':status': {'S': 'pending'}
        }
    )
    
    print(f"顧客: {CUSTOMER_ID}")
    print(f"件数: {response['Count']}")
    
    for item in response['Items'][:5]:
        print(f"  - {item['order_id']['S']}: {item['amount']['N']}円 ({item['order_date']['S']})")
    
    if response['Count'] > 5:
        print(f"  ... 他 {response['Count'] - 5} 件")
    
    return response['Count']


def query_by_status_and_date():
    """クエリ2: ステータス + 日付範囲（FilterExpression 使用）"""
    print("\n=== クエリ2: pending で直近30日の注文 ===")
    
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    response = dynamodb.query(
        TableName=TABLE_NAME,
        IndexName=INDEX_NAME,
        KeyConditionExpression='customer_id = :cid AND #status = :status',
        FilterExpression='order_date BETWEEN :start AND :end',
        ExpressionAttributeNames={
            '#status': 'status'
        },
        ExpressionAttributeValues={
            ':cid': {'S': CUSTOMER_ID},
            ':status': {'S': 'pending'},
            ':start': {'S': start_date},
            ':end': {'S': end_date}
        }
    )
    
    print(f"顧客: {CUSTOMER_ID}")
    print(f"期間: {start_date} 〜 {end_date}")
    print(f"件数: {response['Count']}")
    
    for item in response['Items'][:5]:
        print(f"  - {item['order_id']['S']}: {item['amount']['N']}円 ({item['order_date']['S']})")
    
    return response['Count']


def query_by_status_date_amount():
    """クエリ3: ステータス + 日付範囲 + 金額（FilterExpression 使用）"""
    print("\n=== クエリ3: pending で直近30日、10000円以上の注文 ===")
    
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    min_amount = 10000
    
    response = dynamodb.query(
        TableName=TABLE_NAME,
        IndexName=INDEX_NAME,
        KeyConditionExpression='customer_id = :cid AND #status = :status',
        FilterExpression='order_date BETWEEN :start AND :end AND amount >= :min_amount',
        ExpressionAttributeNames={
            '#status': 'status'
        },
        ExpressionAttributeValues={
            ':cid': {'S': CUSTOMER_ID},
            ':status': {'S': 'pending'},
            ':start': {'S': start_date},
            ':end': {'S': end_date},
            ':min_amount': {'N': str(min_amount)}
        }
    )
    
    print(f"顧客: {CUSTOMER_ID}")
    print(f"期間: {start_date} 〜 {end_date}")
    print(f"最低金額: {min_amount}円")
    print(f"件数: {response['Count']}")
    
    for item in response['Items']:
        print(f"  - {item['order_id']['S']}: {item['amount']['N']}円 ({item['order_date']['S']}) - {item['product_name']['S']}")
    
    return response['Count']


def main():
    print(f"テーブル: {TABLE_NAME}")
    print(f"インデックス: {INDEX_NAME}\n")
    
    count1 = query_by_status()
    count2 = query_by_status_and_date()
    count3 = query_by_status_date_amount()
    
    print("\n=== まとめ ===")
    print(f"クエリ1 (status のみ): {count1} 件")
    print(f"クエリ2 (status + date): {count2} 件")
    print(f"クエリ3 (status + date + amount): {count3} 件")
    
    print("\n【注意】")
    print("現在は FilterExpression を使用していますが、")
    print("2025年11月の新機能では KeyConditionExpression で")
    print("直接複数属性を指定できるようになります。")


if __name__ == '__main__':
    main()
