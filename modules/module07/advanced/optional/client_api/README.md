# DynamoDB Client API サンプル

boto3 の低レベル API (client) を使用した DynamoDB 操作サンプルです。

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

### データ
- `score_data.json` - テーブルにロードするサンプルデータ

### 設定
- `myconfig.py` - テーブル名やセカンダリインデックス名の指定

### テーブル操作
- `create_table.py` - テーブルの作成
- `delete_table.py` - テーブルの削除

### 項目操作
- `put_item.py` - テーブルへの項目の追加
- `get_item.py` - プライマリキーを指定した項目の取得
- `update_item.py` - プライマリキーを指定した条件付きの項目の更新
- `delete_item.py` - プライマリキーを指定した項目の削除

### クエリ操作
- `query.py` - パーティションキーを指定した項目の取得
- `pagenate_scan.py` - scan の結果をページ単位で表示
- `pagenate_query.py` - query の結果をページ単位で表示
- `partQL.py` - PartiQL を使用した項目の取得

### セカンダリインデックス
- `add_gsi.py` - グローバルセカンダリインデックスの作成
- `query_gsi.py` - グローバルセカンダリインデックスへのクエリー実行

## 実行例

```bash
# テーブル作成
python3 create_table.py

# 項目追加
python3 put_item.py

# 項目取得
python3 get_item.py

# クエリ実行
python3 query.py

# GSI作成
python3 add_gsi.py

# GSIクエリ
python3 query_gsi.py

# クリーンアップ
python3 delete_table.py
```

## 参考

- [boto3 DynamoDB Client API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)
- [update_item の ReturnValues パラメータ](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_item.html)
