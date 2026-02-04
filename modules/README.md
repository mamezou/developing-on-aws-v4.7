# Developing on AWS - デモスクリプト

各モジュールのデモスクリプトと実行順序です。

## 実行順序

### 1. 環境確認（Module 03）

```bash
cd modules/module03/python

# Client API vs Resource API の比較
python3 module03_16.py

# DynamoDB テーブル作成（自動クリーンアップ）
python3 module03_26.py
```

### 2. S3 バケット作成（Module 05/06）

```bash
# バケット作成（Resource API）
cd modules/module05/python
python3 module05_28.py

# または Client API
cd modules/module06/python
python3 module06_11.py  # 基本
python3 module06_12.py  # Waiter 付き
```

### 3. DynamoDB テーブル作成（Module 07/08）

```bash
# Client API
cd modules/module07/python
python3 module07_36.py

# Waiter デモ
cd modules/module08/python
python3 module08_17.py
```

## Advanced デモ

### Module 03: SDK Waiter/Paginator

```bash
cd modules/module03/advanced/sdk-waiter-paginator

# S3 データ準備
python3 setup_s3_data.py

# Paginator デモ
python3 paginator_demo.py

# EC2 Waiter デモ（インスタンス起動・終了）
python3 waiter_demo.py
```

### Module 05: S3 Client API

```bash
cd modules/module05/advanced/client_api

# 順番に実行
python3 client01-create-bucket.py
python3 client02-put-object.py
python3 client03-upload-file.py
# ... 以下順番に
python3 client12-delete-bucket.py
```

### Module 07: DynamoDB

```bash
# Client API
cd modules/module07/advanced/client_api
python3 create_table.py
python3 put_item.py
python3 query.py
python3 delete_table.py

# Resource API
cd modules/module07/advanced/resource_api
python3 demo-dynamodb-basic.py
python3 demo-dynamodb-query-scan.py

# Movies サンプル
cd movies_example
python3 Movies00_createTable.py
python3 Movies09_loadData.py
python3 Movies10_query.py
python3 Movies13_deleteTable.py

# GSI マルチキー
cd ../dynamodb-gsi-multi-key
sam deploy --guided --parameter-overrides StudentId=$STUDENT_ID
python3 setup_data.py
python3 query_demo.py
```

### Module 10: Lambda Durable Functions

```bash
cd modules/module10/advanced/lambda-durable-functions

# デプロイ
sam build
sam deploy --guided --parameter-overrides StudentId=$STUDENT_ID

# 実行（README.md 参照）
```

## クリーンアップ

```bash
# S3 バケット削除
aws s3 rb s3://${BUCKET_NAME} --force

# DynamoDB テーブル一覧
aws dynamodb list-tables

# テーブル削除
aws dynamodb delete-table --table-name <TABLE_NAME>
```

## 注意事項

- 各デモは `STUDENT_ID` 環境変数でリソース名を一意化
- EC2 環境では自動設定済み
- ローカル環境では `export STUDENT_ID=your-name` で設定
