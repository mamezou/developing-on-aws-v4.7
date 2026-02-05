"""
X-Ray トレーシングデモ Lambda 関数

X-Ray SDK を使用してサブセグメントを作成し、
処理の詳細をトレースします。
"""
import json
import os
import time
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# boto3 の呼び出しを自動的にトレース
patch_all()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'demo-table'))


def handler(event, context):
    # カスタムサブセグメントを作成
    with xray_recorder.in_subsegment('process_request') as subsegment:
        # アノテーション（検索可能）
        subsegment.put_annotation('request_id', context.aws_request_id)
        
        # メタデータ（検索不可）
        subsegment.put_metadata('event', event)
        
        # ビジネスロジック
        result = process_data()
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'message': 'Traced successfully',
            'request_id': context.aws_request_id,
            'data': result
        })
    }


def process_data():
    """データ処理（DynamoDB 操作）"""
    item_id = f"item-{int(time.time())}"
    timestamp = int(time.time())
    
    # DynamoDB への書き込み（自動的にトレースされる）
    with xray_recorder.in_subsegment('dynamodb_write'):
        table.put_item(Item={
            'id': item_id,
            'timestamp': timestamp,
            'status': 'processed'
        })
    
    # DynamoDB からの読み取り
    with xray_recorder.in_subsegment('dynamodb_read'):
        response = table.get_item(Key={'id': item_id})
    
    # Decimal を int に変換
    item = response.get('Item', {})
    if 'timestamp' in item:
        item['timestamp'] = int(item['timestamp'])
    
    return item
