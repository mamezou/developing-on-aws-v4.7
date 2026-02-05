# SDK Waiter & Paginator デモ

SDK を使うメリットを実感するデモです。手動実装との比較を通じて、SDK の価値を理解します。

## 概要

- **Waiter**: リソースの状態変化を待機
- **Paginator**: 大量データのページング処理

## Part 1: Waiter デモ

DynamoDB テーブルを作成して、ACTIVE 状態になるまで待機します。

### 手動実装（❌ 非推奨）

```python
# 自前でポーリング実装が必要
while True:
    response = dynamodb.describe_table(TableName=table_name)
    status = response['Table']['TableStatus']
    if status == 'ACTIVE':
        break
    time.sleep(2)  # 固定間隔、エラーハンドリングなし
```

### SDK Waiter（✅ 推奨）

```python
waiter = dynamodb.get_waiter('table_exists')
waiter.wait(TableName=table_name)
```

### 実行

```bash
# ディレクトリ移動
cd modules/module03/advanced/sdk-waiter-paginator

python3 waiter_demo.py
```

### 出力例

```
=== 手動ポーリング（非推奨）===
テーブル作成リクエスト: waiter-demo-instructor-1234567890
  ポーリング 1: CREATING
  ポーリング 2: CREATING
  ポーリング 3: ACTIVE
✅ テーブル作成完了（6.2秒、3回ポーリング）

=== Waiter 使用（推奨）===
テーブル作成リクエスト: waiter-demo-instructor-1234567890-waiter
Waiter で待機中...
✅ テーブル作成完了（5.8秒）
```

## Part 2: Paginator デモ

S3 バケット内の大量オブジェクト一覧を取得します。

### 手動実装（❌ 非推奨）

```python
# NextToken の管理が必要
objects = []
response = s3.list_objects_v2(Bucket=bucket_name)
objects.extend(response.get('Contents', []))

while response.get('IsTruncated'):
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        ContinuationToken=response['NextContinuationToken']
    )
    objects.extend(response.get('Contents', []))
```

### SDK Paginator（✅ 推奨）

```python
paginator = s3_client.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket=bucket_name):
    for obj in page.get('Contents', []):
        print(obj['Key'])
```

### 実行

```bash
# 事前準備（ダミーデータ作成）
python3 setup_s3_data.py

# デモ実行
python3 paginator_demo.py
```

## ファイル一覧

- `waiter_demo.py` - DynamoDB Waiter デモ（手動ポーリングとの比較）
- `paginator_demo.py` - S3 Paginator デモ
- `setup_s3_data.py` - ダミーデータ作成スクリプト

## ポイント

- SDK が自動でポーリング間隔を調整
- タイムアウトとエラーハンドリングが組み込み済み
- NextToken の管理が不要
- 「車輪の再発明」を防ぐ
