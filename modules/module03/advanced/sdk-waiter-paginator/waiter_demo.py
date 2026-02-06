"""
DynamoDB Waiter デモ

DynamoDB テーブルを作成して、ACTIVE 状態になるまで待機します。
SDK の Waiter を使うことで、手動ポーリングが不要になります。

【Waiter とは】
- AWS リソースが特定の状態になるまで自動でポーリング
- タイムアウトやリトライ間隔は自動管理
- 手動で while ループを書く必要がない
"""

import boto3
import time
import sys
import os

# スクリプトのディレクトリを基準にパスを解決（どこから実行しても動作）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
from config import STUDENT_ID, REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)

# デモ用テーブル名（タイムスタンプ付き）
DEMO_TABLE_NAME = f"waiter-demo-{STUDENT_ID}-{int(time.time())}"


def demo_without_waiter():
    """Waiter を使わない場合（手動ポーリング）"""
    print("=== 手動ポーリング（非推奨）===")
    print("while ループで状態を確認し続ける必要があります\n")
    
    # テーブル作成
    dynamodb.create_table(
        TableName=DEMO_TABLE_NAME,
        AttributeDefinitions=[{'AttributeName': 'pk', 'AttributeType': 'S'}],
        KeySchema=[{'AttributeName': 'pk', 'KeyType': 'HASH'}],
        BillingMode='PAY_PER_REQUEST'
    )
    print(f"テーブル作成リクエスト: {DEMO_TABLE_NAME}")
    
    # 手動ポーリング
    start = time.time()
    poll_count = 0
    while True:
        poll_count += 1
        response = dynamodb.describe_table(TableName=DEMO_TABLE_NAME)
        status = response['Table']['TableStatus']
        print(f"  ポーリング {poll_count}: {status}")
        
        if status == 'ACTIVE':
            break
        time.sleep(2)  # 2秒待機
    
    elapsed = time.time() - start
    print(f"✅ テーブル作成完了（{elapsed:.1f}秒、{poll_count}回ポーリング）")
    
    # クリーンアップ
    dynamodb.delete_table(TableName=DEMO_TABLE_NAME)
    print(f"テーブル削除: {DEMO_TABLE_NAME}\n")
    time.sleep(5)  # 削除完了を待つ


def demo_with_waiter():
    """Waiter を使う場合（推奨）"""
    print("=== Waiter 使用（推奨）===")
    print("Waiter が自動でポーリングしてくれます\n")
    
    table_name = f"{DEMO_TABLE_NAME}-waiter"
    
    # テーブル作成
    dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[{'AttributeName': 'pk', 'AttributeType': 'S'}],
        KeySchema=[{'AttributeName': 'pk', 'KeyType': 'HASH'}],
        BillingMode='PAY_PER_REQUEST'
    )
    print(f"テーブル作成リクエスト: {table_name}")
    
    # Waiter で待機
    start = time.time()
    waiter = dynamodb.get_waiter('table_exists')
    print("Waiter で待機中...")
    waiter.wait(TableName=table_name)
    
    elapsed = time.time() - start
    print(f"✅ テーブル作成完了（{elapsed:.1f}秒）")
    
    # クリーンアップ
    print(f"\nテーブル削除: {table_name}")
    dynamodb.delete_table(TableName=table_name)
    
    waiter = dynamodb.get_waiter('table_not_exists')
    print("Waiter で削除完了を待機...")
    waiter.wait(TableName=table_name)
    print("✅ テーブル削除完了")


def show_available_waiters():
    """利用可能な Waiter 一覧"""
    print("\n=== DynamoDB で利用可能な Waiter ===")
    for name in dynamodb.waiter_names:
        print(f"  - {name}")
    
    print("\n=== 他のサービスの Waiter 例 ===")
    print("  S3: bucket_exists, bucket_not_exists")
    print("  EC2: instance_running, instance_stopped, instance_terminated")
    print("  RDS: db_instance_available, db_instance_deleted")
    print("  Lambda: function_exists, function_active")


def main():
    print(f"リージョン: {REGION}")
    print(f"テーブル名プレフィックス: {DEMO_TABLE_NAME}\n")
    
    # 手動ポーリング
    demo_without_waiter()
    
    # Waiter 使用
    demo_with_waiter()
    
    # 利用可能な Waiter
    show_available_waiters()
    
    print("\n【まとめ】")
    print("Waiter を使うと:")
    print("  - 手動ポーリングのコードが不要")
    print("  - タイムアウト・リトライ間隔は自動管理")
    print("  - コードがシンプルで可読性向上")


if __name__ == '__main__':
    main()
