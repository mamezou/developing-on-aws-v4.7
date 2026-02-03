# Module 07 - 応用サンプル（自習用）

このディレクトリは講義の補足資料です。

- **基本デモ**: `cli/`, `python/` → 講義中のスライド対応サンプル
- **応用サンプル**: `advanced/` → API比較・自習用の包括的サンプル

## Client API vs Resource API

boto3 には2種類のAPIがあります：

| 項目 | Client API | Resource API |
|------|------------|--------------|
| 作成方法 | `boto3.client('dynamodb')` | `boto3.resource('dynamodb')` |
| 抽象度 | 低レベル（AWS API に近い） | 高レベル（オブジェクト指向） |
| 戻り値 | dict（辞書） | リソースオブジェクト |
| データ形式 | 型記述子付き `{'S': 'value'}` | Python ネイティブ型 |
| 学習コスト | 低い（AWS API ドキュメントと対応） | やや高い |
| 柔軟性 | 高い（全API操作が可能） | 一部制限あり |

### 使い分けの目安

- **Client API**: 細かい制御が必要、PartiQL を使いたい場合
- **Resource API**: シンプルなコードで素早く実装したい場合

## 内容

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

### dynamodb-gsi-multi-key/
GSI マルチ属性キーのデモ（2025年11月新機能対応予定）

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
