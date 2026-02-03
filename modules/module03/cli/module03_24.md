#

## ポーリング
### DynamoDBテーブルの作成

```
aws dynamodb create-table \
    --table-name Notes \
    --attribute-definitions \
        AttributeName=pk,AttributeType=S \
    --key-schema \
        AttributeName=pk,KeyType=HASH \
    --billing-mode=PAY_PER_REQUEST
```

### ステータス取得コマンド

```
aws dynamodb describe-table --table-name Notes --query "Table.TableStatus"
```

## waiterの使用

```
aws dynamodb wait table-exists --table-name Notes
```

## テーブルの削除

```
aws dynamodb delete-table --table-name Notes
```
