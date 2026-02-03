# DynamoDB Resource API サンプル

boto3 の高レベル API (resource) を使用した DynamoDB 操作サンプルです。

AWS公式ドキュメントをベースにしています:
https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/GettingStarted.html

## 準備

```bash
# AWS 認証情報の設定
aws configure
# または
aws sso login --profile <YOUR-PROFILE>

# 認証確認
aws sts get-caller-identity
```

## サンプルファイル一覧

### 基本デモ
- `demo-dynamodb-basic.py` - DynamoDBに対する基本操作
- `demo-dynamodb-query-scan.py` - QueryやScanの実行
- `BatchSample.py` - バッチ操作サンプル

### movies_example/
Moviesテーブルを使った一連の操作サンプル

- `moviedata.json` - サンプルデータ
- `Movies00_createTable.py` - テーブル作成
- `Movies01_putItem.py` - 項目追加
- `Movies02_getItem.py` - 項目取得
- `Movies03_projectionExpression.py` - 射影式を使った取得
- `Movies04_reservedWords.py` - 予約語の扱い
- `Movies05_updateItem.py` - 項目更新
- `Movies06_updateItem.py` - 計算値での更新
- `Movies07_conditionExpression.py` - 条件式を使った更新
- `Movies08_deleteItem.py` - 条件付き削除
- `Movies09_loadData.py` - サンプルデータロード
- `Movies10_query.py` - パーティションキーでクエリ
- `Movies11_query.py` - ソートキー範囲指定クエリ
- `Movies12_scan.py` - スキャン操作
- `Movies13_deleteTable.py` - テーブル削除

### Pagenate-sample/
ページネーションサンプル

- `testdata.json` - サンプルデータ
- `pagenate-test0.py` - テーブル作成とデータ投入
- `pagenate-test1.py` - ScanとLimitの基本
- `pagenate-test2.py` - ページ単位での取得
- `pagenate-test9-delete.py` - テーブル削除

## 実行例

```bash
# movies_example
cd movies_example
python Movies00_createTable.py
python Movies09_loadData.py
python Movies10_query.py
python Movies13_deleteTable.py

# Pagenate-sample
cd Pagenate-sample
python pagenate-test0.py
python pagenate-test1.py
python pagenate-test9-delete.py
```

## 参考

- [boto3 DynamoDB Resource API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#service-resource)
