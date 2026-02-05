# DynamoDB Waiter デモ

DynamoDB テーブル作成時の Waiter 使用方法を確認します。

## 実行方法

```bash
cd modules/module03/cli
```

## 変数定義

```bash
STUDENT_ID=${STUDENT_ID:-instructor}
TABLE_NAME="Notes-${STUDENT_ID}"
echo "TABLE_NAME: ${TABLE_NAME}"
```

## ポーリング

### DynamoDBテーブルの作成

```bash
aws dynamodb create-table \
    --table-name ${TABLE_NAME} \
    --attribute-definitions \
        AttributeName=pk,AttributeType=S \
    --key-schema \
        AttributeName=pk,KeyType=HASH \
    --billing-mode=PAY_PER_REQUEST
```

### ステータス取得コマンド

```bash
aws dynamodb describe-table --table-name ${TABLE_NAME} --query "Table.TableStatus"
```

## waiterの使用

```bash
aws dynamodb wait table-exists --table-name ${TABLE_NAME}
```

## テーブルの削除

```bash
aws dynamodb delete-table --table-name ${TABLE_NAME}
```
