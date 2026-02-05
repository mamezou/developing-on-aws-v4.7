"""
LSI vs GSI 比較デモ: クリーンアップ

テーブルを削除します。
"""
import boto3
from myconfig import TABLE_NAME

dynamodb = boto3.client('dynamodb')

def cleanup():
    print(f"=== テーブル削除: {TABLE_NAME} ===\n")
    
    try:
        dynamodb.delete_table(TableName=TABLE_NAME)
        print("テーブル削除中...")
        
        waiter = dynamodb.get_waiter('table_not_exists')
        waiter.wait(TableName=TABLE_NAME)
        print("✅ 削除完了")
    except dynamodb.exceptions.ResourceNotFoundException:
        print("テーブルは存在しません")

if __name__ == "__main__":
    cleanup()
