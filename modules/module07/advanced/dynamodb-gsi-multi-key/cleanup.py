"""
DynamoDB GSI マルチ属性キー デモ - クリーンアップ

両方のテーブルを削除します。
"""

import boto3
from botocore.exceptions import ClientError
from myconfig import TABLE_TRADITIONAL, TABLE_MULTI_ATTR, REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)


def delete_table(table_name):
    print(f"テーブル削除: {table_name}")
    
    try:
        dynamodb.delete_table(TableName=table_name)
        
        waiter = dynamodb.get_waiter('table_not_exists')
        waiter.wait(TableName=table_name)
        
        print(f"   ✅ 削除完了")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"   ⚠️ 存在しません")
        else:
            raise


def main():
    print("=" * 60)
    print("DynamoDB GSI マルチ属性キー デモ - クリーンアップ")
    print("=" * 60)
    
    delete_table(TABLE_TRADITIONAL)
    delete_table(TABLE_MULTI_ATTR)
    
    print("\n" + "=" * 60)
    print("✅ クリーンアップ完了")
    print("=" * 60)


if __name__ == '__main__':
    main()
