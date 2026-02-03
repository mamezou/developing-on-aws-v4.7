# Lambda Durable Functions デモ

**2025年12月 GA** の新機能。Step Functions を使わずに、コードファーストでマルチステップワークフローを構築します。

## 概要

**Durable Functions** は Lambda の新機能で、以下を実現します：
- チェックポイント＆リプレイ方式で状態を永続化
- `wait` や `callback` 中は Lambda 実行環境を終了（料金ゼロ）
- コードファーストでワークフローを定義

## Step Functions との比較

| 観点 | Durable Functions | Step Functions |
|------|-------------------|----------------|
| 定義方法 | コード（Python/Node.js） | JSON/YAML (ASL) |
| 学習コスト | 低（既存スキル活用） | 中（ASL の習得必要） |
| 可視化 | コードベース | Workflow Studio |
| 複雑なロジック | 得意 | 条件分岐が冗長になりがち |
| 料金 | Lambda 実行時間 | 状態遷移ごと |

## デモシナリオ：EC サイトの注文処理

オンラインショップで高額注文が入った際の承認フローを想定しています。

### ビジネス要件

1. 注文が入ったら在庫を確認する
2. 高額注文は管理者の承認が必要（人間が判断）
3. 承認後に決済処理を行う
4. 決済は外部APIのため、失敗時はリトライが必要
5. 完了したら顧客に通知する

### ワークフロー図

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  注文検証   │ → │  在庫確認   │ → │  承認待ち   │ → │  支払処理   │ → │  完了通知   │
│   (step)    │    │   (step)    │    │ (callback)  │    │(step+retry) │    │   (step)    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                            ↓
                                    Lambda は終了
                                    （課金なし）
                                            ↓
                                    管理者が承認
                                    （数分〜数時間）
                                            ↓
                                    callback で再開
```

### Durable Functions が有効な理由

| ステップ | 課題 | Durable Functions の解決策 |
|----------|------|---------------------------|
| 承認待ち | 人間の判断を待つ間、Lambda を起動し続けると高コスト | `callback` で Lambda を終了、承認後に自動再開 |
| 支払処理 | 外部API障害時のリトライが必要 | `RetryStrategy` で指数バックオフを自動実行 |
| 全体 | 途中で障害が発生した場合の復旧 | チェックポイントから自動再開 |

### 従来の実装との比較

**Step Functions を使う場合：**
- ASL（Amazon States Language）でワークフローを定義
- 状態遷移ごとに課金
- 複雑な条件分岐は JSON が冗長になりがち

**Durable Functions を使う場合：**
- Python/Node.js のコードでワークフローを定義
- Lambda 実行時間のみ課金（待機中は無料）
- 複雑なロジックも通常のコードで記述可能

## 前提条件

- Python 3.12+ または Node.js 22+
- AWS CLI / SAM CLI
- 東京リージョン対応済み

## ファイル一覧

- `app.py` - Lambda 関数コード（Durable Functions SDK 使用）
- `template.yaml` - SAM テンプレート（DurableConfig 設定含む）
- `requirements.txt` - Python 依存パッケージ
- `invoke.sh` - 実行スクリプト（オプション）

## デプロイ

```bash
cd modules/module10/advanced/lambda-durable-functions

# SAM でビルド（Python 3.12 が必要）
sam build

# Python 3.12 がない場合はコンテナビルド
sam build --use-container

# デプロイ（受講生IDを指定）
sam deploy --guided --parameter-overrides StudentId=$STUDENT_ID

# または環境変数が設定されていない場合
sam deploy --guided --parameter-overrides StudentId=instructor
```

### EC2 環境でのデプロイ（推奨）

Code Server 環境では Python 3.12 がプリインストールされています：

```bash
# リポジトリをクローン
git clone https://github.com/mamezou/developing-on-aws-v4.7.git
cd developing-on-aws-v4.7/modules/module10/advanced/lambda-durable-functions

# ビルド＆デプロイ
sam build
sam deploy --guided --parameter-overrides StudentId=$STUDENT_ID
```

## 実行

```bash
# 関数名は StudentId によって変わる（例: order-processing-durable-instructor）
FUNCTION_NAME="order-processing-durable-${STUDENT_ID:-instructor}"

# 注文を開始
aws lambda invoke \
  --function-name $FUNCTION_NAME \
  --payload '{"customer_id": "cust-123", "items": [{"product_id": "prod-001", "price": 1000, "quantity": 2}]}' \
  response.json

# 実行状態の確認
aws lambda list-durable-executions \
  --function-name $FUNCTION_NAME

# 承認コールバックの送信
aws lambda send-durable-execution-callback-success \
  --function-name $FUNCTION_NAME \
  --execution-id <execution-id> \
  --callback-id awaiting-approval \
  --payload '{"approved": true}'
```

## ポイント

1. **チェックポイント**: 各 step 完了時に進捗を永続化
2. **待機中のコスト**: callback 中は Lambda 終了、料金ゼロ
3. **決定論的コード**: リプレイ時に同じ結果を再現する必要あり
4. **リトライ戦略**: カスタムリトライ（指数バックオフ）が可能

## 参考

- [Lambda Durable Functions Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/durable-functions.html)
- [AWS ブログ記事（日本語）](https://aws.amazon.com/jp/blogs/news/build-multi-step-applications-and-ai-workflows-with-aws-lambda-durable-functions/)
