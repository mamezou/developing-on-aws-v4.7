# DynamoDB Local 操作

DynamoDB Local を使用したローカル開発環境でのテーブル操作を確認します。

> **注意**: DynamoDB Local は Docker または Java が必要です。WSL では利用できない場合があります。

## 実行方法

```bash
cd modules/module07/cli
```

## 変数定義

```bash
STUDENT_ID=${STUDENT_ID:-instructor}
TABLE_NAME="Notes-${STUDENT_ID}"
echo "TABLE_NAME: ${TABLE_NAME}"
```

## create table（コマンドプロンプトで実行）

```bash
aws dynamodb create-table --table-name ${TABLE_NAME} --attribute-definitions AttributeName=UserId,AttributeType=S --key-schema AttributeName=UserId,KeyType=HASH --billing-mode=PAY_PER_REQUEST --endpoint http://localhost:8000

aws dynamodb list-tables --endpoint http://localhost:8000
```

## put item

```bash
aws dynamodb put-item --table-name ${TABLE_NAME} --item "{\"UserId\":{\"S\":\"StudentA\"},\"NoteId\":{\"N\":\"11\"},\"Note\":{\"S\":\"HelloWorld!\"}}" --endpoint http://localhost:8000
```

## scan

```bash
aws dynamodb scan --table-name ${TABLE_NAME} --endpoint http://localhost:8000
```

## delete table

```bash
aws dynamodb delete-table --table-name ${TABLE_NAME} --endpoint http://localhost:8000
```
