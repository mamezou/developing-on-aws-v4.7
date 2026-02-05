# Lambda Durable Functions デモ

Step Functions を使わずに、コードファーストでマルチステップワークフローを構築するデモです。

> Durable Functions は **2025年12月リリース**（re:Invent 2025 発表）の新機能です。

## Durable Functions の仕組み

- `@durable_step` デコレータで各ステップにチェックポイント作成
- `context.wait()` 実行時は Lambda 実行環境を終了（料金ゼロ）
- 再開時は新しい実行環境でリプレイし、完了済みステップはスキップ
- 公式 SDK: `aws_durable_execution_sdk_python`（ランタイムに含まれる）

## Step Functions との比較

| 観点 | Durable Functions | Step Functions |
|------|-------------------|----------------|
| 定義方法 | コード（Python/Node.js） | JSON/YAML (ASL) |
| 学習コスト | 低（既存スキル活用） | 中（ASL の習得必要） |
| 複雑なロジック | 得意 | 条件分岐が冗長になりがち |

## デモシナリオ

```
注文受付 → 在庫確認 → 承認待ち → 支払い処理 → 完了通知
   ↓          ↓          ↓           ↓
 (step)    (step)    (wait)      (step+retry)
```

## 実行方法

```bash
# ディレクトリ移動
cd modules/module11/advanced/lambda-durable-functions
```

### 1. IAM ロールの作成

```bash
# IAM ロールを作成
aws iam create-role \
  --role-name lambda-durable-demo-role \
  --assume-role-policy-document file://trust-policy.json

# Lambda 実行ポリシーをアタッチ
aws iam attach-role-policy \
  --role-name lambda-durable-demo-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Durable Functions 用の権限を追加
aws iam put-role-policy \
  --role-name lambda-durable-demo-role \
  --policy-name DurableFunctionsPolicy \
  --policy-document file://durable-policy.json

# IAM ロールの伝播を待機
sleep 10
```

### 2. Lambda 関数の作成

> **注意**: AWS CLI 2.33.x では `--durable-function-configuration` オプションがまだサポートされていないため、boto3 を使用します。

```bash
python3 deploy.py
```

### 3. 注文の開始

```bash
# Durable Functions は非同期呼び出しが必要（バージョン指定）
aws lambda invoke \
  --function-name order-processing-durable:1 \
  --invocation-type Event \
  --payload '{"order_id": "order-123", "items": [{"product_id": "prod-001", "name": "Widget", "price": 1000, "quantity": 2}]}' \
  response.json
```

### 4. 実行状態の確認

```bash
# 実行一覧を取得
aws lambda list-durable-executions \
  --function-name order-processing-durable:1

# 特定の実行の詳細を確認（ARN は list-durable-executions の出力から取得）
aws lambda get-durable-execution \
  --durable-execution-arn <DurableExecutionArn>
```

### 5. クリーンアップ

```bash
aws lambda delete-function --function-name order-processing-durable

aws iam detach-role-policy \
  --role-name lambda-durable-demo-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam delete-role-policy \
  --role-name lambda-durable-demo-role \
  --policy-name DurableFunctionsPolicy

aws iam delete-role --role-name lambda-durable-demo-role

rm -f function.zip response.json
```

## ファイル

- `app.py` - 注文処理ワークフローの実装
- `deploy.py` - Lambda 関数デプロイスクリプト（boto3）
- `trust-policy.json` - IAM ロールの信頼ポリシー
- `durable-policy.json` - Durable Functions 用の権限ポリシー

## 参考リンク

- [Lambda Durable Functions Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/durable-functions.html)
- [AWS ブログ記事](https://aws.amazon.com/blogs/aws/build-multi-step-applications-and-ai-workflows-with-aws-lambda-durable-functions/)
