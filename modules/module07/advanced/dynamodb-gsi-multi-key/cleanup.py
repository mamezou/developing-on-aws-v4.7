"""
DynamoDB GSI マルチ属性キー デモ - クリーンアップ

テーブルを削除します。
"""

import boto3
from botocore.exceptions import ClientError
from myconfig import TABLE_NAME, REGION

dynamodb = boto3.client('dynamodb', region_name=REGION)


def delete_table():
    print(f"テーブル削除: {TABLE_NAME}")
    
    try:
        dynamodb.delete_table(TableName=TABLE_NAME)
        
        # テーブルが削除されるまで待機
        waiter = dynamodb.get_waiter('table_not_exists')
        waiter.wait(TableName=TABLE_NAME)
        
        print(f"✅ テーブル削除完了: {TABLE_NAME}")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"⚠️ テーブルは存在しません: {TABLE_NAME}")
        else:
            raise


if __name__ == '__main__':
    delete_table()
