# Module 07 - 応用サンプル（自習用）

このディレクトリは講義の補足資料です。

- **基本デモ**: `cli/`, `python/` → 講義中のスライド対応サンプル
- **応用サンプル**: `advanced/` → API比較・自習用の包括的サンプル

## 内容

boto3 の Client API と Resource API の違いを比較できます。

### client_api/
低レベル API (boto3.client) を使用した DynamoDB 操作
- テーブル作成/削除
- 項目操作（put, get, update, delete）
- Query / Scan / PartiQL
- ページネーション
- GSI（グローバルセカンダリインデックス）

### resource_api/
高レベル API (boto3.resource) を使用した DynamoDB 操作
- movies_example/: AWS公式ドキュメントベースのサンプル
- Pagenate-sample/: ページネーションサンプル
- バッチ操作サンプル

## 主なサンプル

| 操作 | client_api | resource_api |
|------|------------|--------------|
| テーブル作成 | create_table.py | movies_example/Movies00_createTable.py |
| 項目追加 | put_item.py | movies_example/Movies01_putItem.py |
| 項目取得 | get_item.py | movies_example/Movies02_getItem.py |
| 項目更新 | update_item.py | movies_example/Movies05_updateItem.py |
| クエリ | query.py | movies_example/Movies10_query.py |
| スキャン | pagenate_scan.py | movies_example/Movies12_scan.py |
| GSI | add_gsi.py, query_gsi.py | - |

## 参考

- 元リポジトリ: https://github.com/tetsuo-nobe/dev_on_aws
- [AWS DynamoDB Getting Started](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/GettingStarted.html)
