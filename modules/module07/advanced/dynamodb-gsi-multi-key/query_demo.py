"""
DynamoDB GSI マルチ属性キー デモ - クエリ比較

従来方式とマルチ属性キー方式で同じクエリを実行し、コードの違いを比較します。
"""

import boto3
from datetime import datetime, timedelta
from myconfig import TABLE_TRADITIONAL, TABLE_MULTI_ATTR, INDEX_NAME, REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)

CUSTOMER_ID = 'CUST-001'
TARGET_STATUS = 'pending'


def query_traditional_status_only():
    """
    従来方式: ステータスのみでクエリ
    合成キーの前方一致（begins_with）を使用
    """
    print("\n" + "-" * 50)
    print("📦 従来方式: pending の注文を取得")
    print("-" * 50)
    
    # 合成キーの前方一致でクエリ
    prefix = f"{TARGET_STATUS}#"
    
    print(f"   KeyConditionExpression:")
    print(f"     customer_id = '{CUSTOMER_ID}'")
    print(f"     AND begins_with(composite_sk, '{prefix}')")
    
    response = dynamodb.query(
        TableName=TABLE_TRADITIONAL,
        IndexName=INDEX_NAME,
        KeyConditionExpression='customer_id = :cid AND begins_with(composite_sk, :prefix)',
        ExpressionAttributeValues={
            ':cid': {'S': CUSTOMER_ID},
            ':prefix': {'S': prefix},
        }
    )
    
    print(f"\n   結果: {response['Count']} 件")
    for item in response['Items'][:3]:
        print(f"     - {item['order_id']['S']}: {item['amount']['N']}円 ({item['order_date']['S']})")
    if response['Count'] > 3:
        print(f"     ... 他 {response['Count'] - 3} 件")
    
    return response['Count']


def query_multi_attr_status_only():
    """
    マルチ属性キー方式: ステータスのみでクエリ
    直接属性を指定（合成キー不要！）
    """
    print("\n" + "-" * 50)
    print("🚀 マルチ属性キー方式: pending の注文を取得")
    print("-" * 50)
    
    print(f"   KeyConditionExpression:")
    print(f"     customer_id = '{CUSTOMER_ID}'")
    print(f"     AND status = '{TARGET_STATUS}'")
    
    response = dynamodb.query(
        TableName=TABLE_MULTI_ATTR,
        IndexName=INDEX_NAME,
        KeyConditionExpression='customer_id = :cid AND #status = :status',
        ExpressionAttributeNames={
            '#status': 'status'  # status は予約語
        },
        ExpressionAttributeValues={
            ':cid': {'S': CUSTOMER_ID},
            ':status': {'S': TARGET_STATUS},
        }
    )
    
    print(f"\n   結果: {response['Count']} 件")
    for item in response['Items'][:3]:
        print(f"     - {item['order_id']['S']}: {item['amount']['N']}円 ({item['order_date']['S']})")
    if response['Count'] > 3:
        print(f"     ... 他 {response['Count'] - 3} 件")
    
    return response['Count']


def query_traditional_status_and_date():
    """
    従来方式: ステータス + 日付範囲でクエリ
    合成キーの前方一致 + FilterExpression が必要
    """
    print("\n" + "-" * 50)
    print("📦 従来方式: pending で直近30日の注文を取得")
    print("-" * 50)
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # 合成キーでは日付範囲を KeyCondition で指定できない
    # FilterExpression を使う必要がある（効率が悪い）
    prefix = f"{TARGET_STATUS}#"
    
    print(f"   KeyConditionExpression:")
    print(f"     customer_id = '{CUSTOMER_ID}'")
    print(f"     AND begins_with(composite_sk, '{prefix}')")
    print(f"   FilterExpression:")
    print(f"     order_date BETWEEN '{start_date}' AND '{end_date}'")
    print(f"   ⚠️ FilterExpression は読み取り後にフィルタ（非効率）")
    
    response = dynamodb.query(
        TableName=TABLE_TRADITIONAL,
        IndexName=INDEX_NAME,
        KeyConditionExpression='customer_id = :cid AND begins_with(composite_sk, :prefix)',
        FilterExpression='order_date BETWEEN :start AND :end',
        ExpressionAttributeValues={
            ':cid': {'S': CUSTOMER_ID},
            ':prefix': {'S': prefix},
            ':start': {'S': start_date},
            ':end': {'S': end_date},
        }
    )
    
    print(f"\n   結果: {response['Count']} 件")
    print(f"   ScannedCount: {response['ScannedCount']} 件（読み取り後フィルタ）")
    
    return response['Count'], response['ScannedCount']


def query_multi_attr_status_and_date():
    """
    マルチ属性キー方式: ステータス + 日付範囲でクエリ
    KeyConditionExpression で直接指定可能！
    """
    print("\n" + "-" * 50)
    print("🚀 マルチ属性キー方式: pending で直近30日の注文を取得")
    print("-" * 50)
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"   KeyConditionExpression:")
    print(f"     customer_id = '{CUSTOMER_ID}'")
    print(f"     AND status = '{TARGET_STATUS}'")
    print(f"     AND order_date BETWEEN '{start_date}' AND '{end_date}'")
    print(f"   ✅ FilterExpression 不要！効率的！")
    
    response = dynamodb.query(
        TableName=TABLE_MULTI_ATTR,
        IndexName=INDEX_NAME,
        KeyConditionExpression='customer_id = :cid AND #status = :status AND order_date BETWEEN :start AND :end',
        ExpressionAttributeNames={
            '#status': 'status'
        },
        ExpressionAttributeValues={
            ':cid': {'S': CUSTOMER_ID},
            ':status': {'S': TARGET_STATUS},
            ':start': {'S': start_date},
            ':end': {'S': end_date},
        }
    )
    
    print(f"\n   結果: {response['Count']} 件")
    print(f"   ScannedCount: {response['ScannedCount']} 件（読み取り = 結果）")
    
    return response['Count'], response['ScannedCount']


def main():
    print("=" * 60)
    print("DynamoDB GSI マルチ属性キー デモ - クエリ比較")
    print("=" * 60)
    print(f"\n対象顧客: {CUSTOMER_ID}")
    
    # クエリ1: ステータスのみ
    print("\n" + "=" * 60)
    print("【クエリ1】ステータスのみで絞り込み")
    print("=" * 60)
    
    count_trad_1 = query_traditional_status_only()
    count_multi_1 = query_multi_attr_status_only()
    
    # クエリ2: ステータス + 日付範囲
    print("\n" + "=" * 60)
    print("【クエリ2】ステータス + 日付範囲で絞り込み")
    print("=" * 60)
    
    count_trad_2, scanned_trad_2 = query_traditional_status_and_date()
    count_multi_2, scanned_multi_2 = query_multi_attr_status_and_date()
    
    # まとめ
    print("\n" + "=" * 60)
    print("【まとめ】")
    print("=" * 60)
    
    print("\n📊 クエリ1（ステータスのみ）:")
    print(f"   従来方式: {count_trad_1} 件")
    print(f"   マルチ属性キー: {count_multi_1} 件")
    
    print("\n📊 クエリ2（ステータス + 日付範囲）:")
    print(f"   従来方式: {count_trad_2} 件 (読み取り: {scanned_trad_2} 件)")
    print(f"   マルチ属性キー: {count_multi_2} 件 (読み取り: {scanned_multi_2} 件)")
    
    print("\n💡 ポイント:")
    print("   1. マルチ属性キーでは合成キーの作成・パースが不要")
    print("   2. KeyConditionExpression で複数属性を直接指定可能")
    print("   3. FilterExpression が不要になり、読み取り効率が向上")
    print("   4. コードがシンプルで保守しやすい")


if __name__ == '__main__':
    main()
