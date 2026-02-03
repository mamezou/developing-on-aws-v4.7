## create table（コマンドプロンプトで実行）
aws dynamodb create-table --table-name Notes --attribute-definitions AttributeName=UserId,AttributeType=S --key-schema AttributeName=UserId,KeyType=HASH --billing-mode=PAY_PER_REQUEST --endpoint http://localhost:8000

aws dynamodb list-tables --endpoint http://localhost:8000

## put item
aws dynamodb put-item --table-name Notes --item "{\"UserId\":{\"S\":\"StudentA\"},\"NoteId\":{\"N\":\"11\"},\"Note\":{\"S\":\"HelloWorld!\"}}" --endpoint http://localhost:8000

## scan
aws dynamodb scan --table-name Notes --endpoint http://localhost:8000

## delete table
aws dynamodb delete-table --table-name Notes --endpoint http://localhost:8000
