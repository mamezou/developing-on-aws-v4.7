# Developing on AWS v4.7 サンプルコード

このリポジトリでは [Developing on AWS v4.7](https://aws.amazon.com/jp/training/classroom/developing-on-aws/) で使用するサンプルコードを管理しています。

## ディレクトリ構成

```
developing-on-aws-v4.7/
├── README.md           # このファイル
├── config.py           # 共通設定（STUDENT_ID, BUCKET_NAME 等）
├── modules/            # モジュール別デモコード
│   ├── module03/       # アクセス許可（IAM）+ SDK基礎
│   ├── module04/       # ストレージ（S3基礎）
│   ├── module05/       # ストレージオペレーション（S3操作）
│   ├── module06/       # データベース（DynamoDB基礎）
│   ├── module07/       # データベースオペレーション（DynamoDB操作）
│   ├── module08/       # アプリケーションロジック（Lambda）
│   ├── module09/       # API管理（API Gateway）
│   ├── module10/       # モダンアプリケーション（Step Functions）
│   ├── module11/       # アプリケーションユーザー（Cognito）
│   ├── module12/       # アプリケーションデプロイ（SAM）
│   ├── module13/       # SAM CLI
│   └── module14/       # アプリケーション監視（CloudWatch, X-Ray）
└── infra/              # インフラコード（受講者環境用）
    └── cdk/
```

## 前提条件

- Python 3.x
- boto3 1.34+
- AWS CLI v2

```bash
# boto3 インストール
pip install boto3

# AWS CLI 設定確認
aws sts get-caller-identity
```

## 事前準備

### 1. AWS 認証情報の設定

デモ実行前に AWS にログインしてください。

```bash
# IAM Identity Center (SSO) の場合
aws sso login --profile <YOUR-PROFILE>

# アクセスキーの場合
aws configure

# 認証確認
aws sts get-caller-identity
```

### 2. リソース名について

サンプルコードは `config.py` を使用して、受講者ごとに一意のリソース名を自動生成します。

```
バケット名: dev-on-aws-{student_id}-{account_id}
例: dev-on-aws-student-1-123456789012
```

設定変更は不要です。そのまま実行できます。

## 使い方

各モジュールの README を参照してください。

| モジュール | 内容 | README / デモ |
|-----------|------|---------------|
| Module 03 | SDK Waiter & Paginator | [sdk-waiter-paginator](modules/module03/advanced/sdk-waiter-paginator/README.md) |
| Module 05 | S3 Client API / Resource API | [client_api](modules/module05/advanced/client_api/README.md), [resource_api](modules/module05/advanced/resource_api/README.md) |
| Module 07 | DynamoDB GSI / LSI 比較 | [lsi-gsi-comparison](modules/module07/advanced/lsi-gsi-comparison/README.md), [dynamodb-gsi-multi-key](modules/module07/advanced/dynamodb-gsi-multi-key/README.md) |
| Module 10 | API Gateway Swagger インポート | [swagger-import](modules/module10/advanced/swagger-import/README.md) |
| Module 11 | Lambda Durable Functions / Strangler Fig | [lambda-durable-functions](modules/module11/advanced/lambda-durable-functions/README.md), [strangler-fig-pattern](modules/module11/advanced/strangler-fig-pattern/README.md) |
| Module 12 | Cognito API Authorizer | [cognito-api-authorizer](modules/module12/advanced/cognito-api-authorizer/README.md) |
| Module 14 | X-Ray トレーシング | [xray-tracing](modules/module14/advanced/xray-tracing/README.md) |

### CLI サンプル

各モジュールの `cli/` ディレクトリに Markdown ファイルがあります。コードブロック内のコマンドをターミナルで実行してください。

### Python サンプル

各モジュールの `python/` ディレクトリに Python スクリプトがあります。

```bash
# ルートディレクトリからでも実行可能
python3 modules/module05/python/module05_28.py

# または各ディレクトリで実行
cd modules/module05/python
python3 module05_28.py
```

## モジュール構成

各モジュールのディレクトリには以下が含まれます：
- `cli/` - AWS CLI コマンドサンプル（Markdown）
- `python/` - Python (boto3) サンプル
- `advanced/` - 応用デモ（一部モジュールのみ）

## 参考リンク

- [AWS SDK for Python (boto3) ドキュメント](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS CLI コマンドリファレンス](https://docs.aws.amazon.com/cli/latest/reference/)
