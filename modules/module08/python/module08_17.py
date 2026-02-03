import boto3

dynamodb = boto3.client('dynamodb')

table = dynamodb.create_table(
    TableName="Notes",
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

print('テーブル作成をリクエストしました')

waiter = dynamodb.get_waiter('table_exists')
waiter.wait(TableName="Notes")

print('テーブルを作成できました')
