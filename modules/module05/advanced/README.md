# Module 05 - 応用サンプル（自習用）

このディレクトリは講義の補足資料です。

- **基本デモ**: `cli/`, `python/` → 講義中のスライド対応サンプル
- **応用サンプル**: `advanced/` → API比較・自習用の包括的サンプル

## Client API vs Resource API

boto3 には2種類のAPIがあります：

| 項目 | Client API | Resource API |
|------|------------|--------------|
| 作成方法 | `boto3.client('s3')` | `boto3.resource('s3')` |
| 抽象度 | 低レベル（AWS API に近い） | 高レベル（オブジェクト指向） |
| 戻り値 | dict（辞書） | リソースオブジェクト |
| 学習コスト | 低い（AWS API ドキュメントと対応） | やや高い |
| 柔軟性 | 高い（全API操作が可能） | 一部制限あり |
| コード量 | 多め | 少なめ |

### 使い分けの目安

- **Client API**: 細かい制御が必要、最新機能を使いたい場合
- **Resource API**: シンプルなコードで素早く実装したい場合

## 内容

### client_api/
低レベル API (boto3.client) を使用した S3 操作

### resource_api/
高レベル API (boto3.resource) を使用した S3 操作

## 主なサンプル

| 操作 | client_api | resource_api |
|------|------------|--------------|
| バケット一覧 | client00-list-bucket.py | resource00-list-bucket.py |
| バケット作成 | client01-create-bucket.py | resource01-create-bucket.py |
| オブジェクト格納 | client02-put-object.py | resource02-put-object.py |
| ファイルアップロード | client03-upload-file.py | resource03-upload-file.py |
| オブジェクト取得 | client04-get-object.py | resource04-get-object.py |
| マルチパートアップロード | client09-multipart-upload.py | resource08-multipart-upload.py |
| 署名付きURL | client11-presigned_url.py | resource10-presigned_url.py |

## バケット名について

`mybucket.py` は `config.py` と連携しており、環境変数 `STUDENT_ID` に基づいて動的にバケット名が生成されます。

## 参考

- 元リポジトリ: https://github.com/tetsuo-nobe/dev_on_aws
