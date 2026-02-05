# Developing on AWS v4.7 サンプルコード

このリポジトリでは [Developing on AWS v4.7](https://aws.amazon.com/jp/training/classroom/developing-on-aws/) で使用するサンプルコードを管理しています。

## ディレクトリ構成

```
developing-on-aws-v4.7/
├── README.md           # このファイル
├── modules/            # モジュール別デモコード
│   ├── module03/       # アクセス許可
│   ├── module04/       # ストレージ（S3基礎）
│   ├── module05/       # Storage 1
│   ├── module06/       # Storage 2
│   ├── module07/       # Database 1
│   ├── module08/       # Database 2
│   ├── module09/       # Lambda詳細
│   ├── module10/       # Step Functions
│   └── module13/       # SAM CLI
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

| モジュール | 内容 | README |
|-----------|------|--------|
| Module 03 | SDK Waiter & Paginator | [advanced/sdk-waiter-paginator](modules/module03/advanced/sdk-waiter-paginator/README.md) |
| Module 05 | S3 操作 | [advanced](modules/module05/advanced/README.md) |
| Module 07 | DynamoDB / LSI vs GSI | [advanced](modules/module07/advanced/README.md) |

### CLI サンプル

各モジュールの `cli/` ディレクトリに Markdown ファイルがあります。コードブロック内のコマンドをターミナルで実行してください。

### Python サンプル

各モジュールの `python/` ディレクトリに Python スクリプトがあります。

```bash
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
