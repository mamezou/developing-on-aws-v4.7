import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
    TableName='Notes',
    AttributeDefinitions=[
        {
            'AttributeName': 'pk',
            'AttributeType': 'S'
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'pk',
            'KeyType': 'HASH'
        }
    ],
    BillingMode='PAY_PER_REQUEST',
)

print('テーブルの作成をリクエストしました。')
table.meta.client.get_waiter('table_exists').wait(TableName='Notes')
print('テーブルの作成が完了しました。')

print(table.item_count)

# CLI:テーブルの削除
# aws dynamodb delete-table --table-name Notes
