"""
LSI vs GSI 比較デモ: クエリ実行

同じデータに対して、テーブル/LSI/GSI それぞれでクエリを実行し、
用途の違いを体験します。
"""
import boto3
from boto3.dynamodb.conditions import Key
from myconfig import TABLE_NAME, LSI_NAME, GSI_NAME

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def query_base_table():
    """ベーステーブル: 顧客の注文を日付順で取得"""
    print("=" * 60)
    print("【ベーステーブル】田中さんの注文を日付順で取得")
    print("  PK: customer_id, SK: order_date")
    print("=" * 60)
    
    response = table.query(
        KeyConditionExpression=Key('customer_id').eq('tanaka')
    )
    
    print("\n  日付順（デフォルト）:")
    for item in response['Items']:
        print(f"    {item['order_date']}: {item['product_id']} ¥{int(item['amount']):,}")

def query_lsi():
    """LSI: 同じ顧客の注文を金額順で取得"""
    print("\n" + "=" * 60)
    print(f"【LSI: {LSI_NAME}】田中さんの注文を金額順で取得")
    print("  PK: customer_id（同じ）, SK: amount（別の軸）")
    print("  → 同じ顧客内で、ソートの切り口を変えたい場合に使う")
    print("=" * 60)
    
    # 金額の高い順
    response = table.query(
        IndexName=LSI_NAME,
        KeyConditionExpression=Key('customer_id').eq('tanaka'),
        ScanIndexForward=False  # 降順
    )
    
    print("\n  金額の高い順:")
    for item in response['Items']:
        print(f"    ¥{int(item['amount']):,}: {item['product_id']} ({item['order_date']})")
    
    # 金額でフィルタ（1万円以上）
    response = table.query(
        IndexName=LSI_NAME,
        KeyConditionExpression=Key('customer_id').eq('tanaka') & Key('amount').gte(10000)
    )
    
    print("\n  1万円以上の注文:")
    for item in response['Items']:
        print(f"    ¥{int(item['amount']):,}: {item['product_id']}")

def query_gsi():
    """GSI: 商品ごとの売上を取得"""
    print("\n" + "=" * 60)
    print(f"【GSI: {GSI_NAME}】LAPTOP01の売上を日付順で取得")
    print("  PK: product_id（全く別の軸）, SK: order_date")
    print("  → 顧客とは関係なく、商品軸で検索したい場合に使う")
    print("=" * 60)
    
    response = table.query(
        IndexName=GSI_NAME,
        KeyConditionExpression=Key('product_id').eq('LAPTOP01')
    )
    
    print("\n  LAPTOP01 の売上履歴:")
    total = 0
    for item in response['Items']:
        print(f"    {item['order_date']}: {item['customer_id']}さん ¥{int(item['amount']):,}")
        total += int(item['amount'])
    print(f"\n  合計: ¥{total:,}（{len(response['Items'])}件）")
    
    # 別の商品
    print("\n  KEYBOARD01 の売上履歴:")
    response = table.query(
        IndexName=GSI_NAME,
        KeyConditionExpression=Key('product_id').eq('KEYBOARD01')
    )
    total = 0
    for item in response['Items']:
        print(f"    {item['order_date']}: {item['customer_id']}さん ¥{int(item['amount']):,}")
        total += int(item['amount'])
    print(f"\n  合計: ¥{total:,}（{len(response['Items'])}件）")

def show_summary():
    """まとめ"""
    print("\n" + "=" * 60)
    print("【まとめ】LSI vs GSI の使い分け")
    print("=" * 60)
    print("""
┌────────────────────────────────────────────────────────┐
│ LSI: 同じ顧客（PK）の中で、別の軸でソートしたい       │
│      例）田中さんの注文を「金額順」で見たい           │
│      → customer_id は変えず、ソートキーだけ変える    │
├────────────────────────────────────────────────────────┤
│ GSI: 全く別の軸で検索したい                           │
│      例）「この商品」がいつ、誰に売れたか見たい       │
│      → 顧客とは無関係に、商品軸で検索                │
└────────────────────────────────────────────────────────┘

【実務での選択基準】
- 設計が固まっていない → GSI（後から追加できる）
- 10GB超えそう → GSI（LSIはパーティションあたり10GB制限）
- 強い整合性が必要 → LSI（GSIは結果整合性のみ）
""")

if __name__ == "__main__":
    query_base_table()
    query_lsi()
    query_gsi()
    show_summary()
    print(f"\nクリーンアップ: python3 cleanup.py")
