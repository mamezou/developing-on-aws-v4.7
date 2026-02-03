import sys
sys.path.insert(0, '../../../')
from config import TABLE_NAME
import boto3

dynamodb = boto3.client('dynamodb')

table = dynamodb.create_table(
    TableName=TABLE_NAME,
    AttributeDefinitions=[
        {
            'AttributeName': 'UserId',
            'AttributeType': 'S'
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'UserId',
            'KeyType': 'HASH'
        }
    ],
    BillingMode='PAY_PER_REQUEST',
)

print(f'テーブル {TABLE_NAME} の作成をリクエストしました')

waiter = dynamodb.get_waiter('table_exists')
waiter.wait(TableName=TABLE_NAME)

print('テーブルを作成できました')
