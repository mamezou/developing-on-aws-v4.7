# Developing on AWS v4.7 サンプルコード

このリポジトリでは [Developing on AWS v4.7](https://aws.amazon.com/jp/training/classroom/developing-on-aws/) で使用するサンプルコードを管理しています。

## ディレクトリ構成

```
developing-on-aws-v4.7/
├── README.md           # このファイル
├── modules/            # モジュール別デモコード
│   ├── module03/       # アクセス許可
│   ├── module04/       # ストレージ（S3基礎）
│   ├── module05/       # ストレージオペレーション
│   ├── module06/       # データベース（DynamoDB基礎）
│   ├── module07/       # データベースオペレーション
│   ├── module08/       # Lambda
│   ├── module09/       # API Gateway
│   ├── module10/       # モダンアプリケーション
│   └── module13/       # 監視（X-Ray）
├── demo/               # 追加デモ
│   ├── lambda-durable-functions/
│   ├── sdk-waiter-paginator/
│   └── dynamodb-gsi-multi-key/
└── infra/              # インフラコード（受講者環境用）
    ├── cdk/
    └── scripts/
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

### CLI サンプル

各モジュールの `cli/` ディレクトリにMarkdownファイルがあります。コードブロック内のコマンドをターミナルで実行してください。

### Python サンプル

各モジュールの `python/` ディレクトリにPythonスクリプトがあります。

```bash
cd modules/module05/python
python module05_28.py
```

## モジュール構成

各モジュールのディレクトリには以下が含まれます：
- `cli/` - AWS CLI コマンドサンプル（Markdown）
- `python/` - Python (boto3) サンプル
- `advanced/` - 応用デモ（一部モジュールのみ）

## 追加デモ

### Lambda Durable Functions (Module 8/10)
2024年12月リリースの新機能。コードファーストでマルチステップワークフローを構築。

### SDK Waiter & Paginator (Module 2)
SDKを使うメリットを実感するデモ。手動実装との比較。

### DynamoDB GSI マルチ属性キー (Module 6/7)
2025年11月リリースの新機能。合成キー不要で複合条件クエリが可能。

## 参考リンク

- [AWS SDK for Python (boto3) ドキュメント](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS CLI コマンドリファレンス](https://docs.aws.amazon.com/cli/latest/reference/)
