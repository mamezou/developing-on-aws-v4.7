"""
Module 08: Waiter のポーリング動作を可視化

デモ内容:
- Waiter が内部でどのようにポーリングしているかを可視化
- ポーリング間隔、最大試行回数の確認
- カスタム Waiter 設定の例

実行方法:
  python3 module08_17.py
"""
import sys
sys.path.insert(0, '../../../')
from config import STUDENT_ID
import boto3
import time

DEMO_TABLE_NAME = f"demo-waiter-{STUDENT_ID}-{int(time.time())}"

def main():
    dynamodb = boto3.client('dynamodb')
    
    print("=== Waiter ポーリング動作デモ ===\n")
    
    # Waiter の設定を確認
    print("1. Waiter のデフォルト設定を確認")
    waiter = dynamodb.get_waiter('table_exists')
    print(f"   ポーリング間隔: {waiter.config.delay}秒")
    print(f"   最大試行回数: {waiter.config.max_attempts}回")
    print(f"   → 最大待機時間: {waiter.config.delay * waiter.config.max_attempts}秒\n")
    
    # テーブル作成
    print(f"2. テーブル作成: {DEMO_TABLE_NAME}")
    dynamodb.create_table(
        TableName=DEMO_TABLE_NAME,
        AttributeDefinitions=[
            {'AttributeName': 'UserId', 'AttributeType': 'S'}
        ],
        KeySchema=[
            {'AttributeName': 'UserId', 'KeyType': 'HASH'}
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    print("   リクエスト送信完了\n")
    
    # 手動ポーリングで動作を可視化
    print("3. ポーリング動作を可視化（手動実装）")
    poll_count = 0
    start = time.time()
    
    while True:
        poll_count += 1
        response = dynamodb.describe_table(TableName=DEMO_TABLE_NAME)
        status = response['Table']['TableStatus']
        elapsed = time.time() - start
        print(f"   [{poll_count}回目] {elapsed:.1f}秒経過 - 状態: {status}")
        
        if status == 'ACTIVE':
            break
        time.sleep(2)  # 2秒間隔でポーリング
    
    print(f"\n   ✅ テーブル作成完了（{poll_count}回のポーリング、{elapsed:.1f}秒）\n")
    
    # Waiter を使った場合との比較
    print("4. 参考: Waiter を使うと上記が1行で書ける")
    print("   waiter = dynamodb.get_waiter('table_exists')")
    print("   waiter.wait(TableName=TABLE_NAME)")
    print("   → 内部で同様のポーリングを自動実行\n")
    
    # カスタム設定の例
    print("5. カスタム Waiter 設定の例")
    print("   from botocore.config import Config")
    print("   waiter.wait(")
    print("       TableName=TABLE_NAME,")
    print("       WaiterConfig={'Delay': 5, 'MaxAttempts': 10}")
    print("   )")
    print("   → ポーリング間隔5秒、最大10回に変更\n")
    
    # クリーンアップ
    print("6. クリーンアップ...")
    dynamodb.delete_table(TableName=DEMO_TABLE_NAME)
    waiter = dynamodb.get_waiter('table_not_exists')
    waiter.wait(TableName=DEMO_TABLE_NAME)
    print("   ✅ 削除完了")

if __name__ == "__main__":
    main()
