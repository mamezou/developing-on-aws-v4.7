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

# テーブルの削除
# dynamodb.delete_table(TableName="Notes")

# テーブルの一覧表示
# aws dynamodb list-tables
