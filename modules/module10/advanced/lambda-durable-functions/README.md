# Lambda Durable Functions デモ

2024年12月リリースの新機能。Step Functions を使わずに、コードファーストでマルチステップワークフローを構築します。

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

## デモシナリオ

注文処理ワークフロー：
```
注文受付 → 在庫確認 → 承認待ち → 支払い処理 → 完了通知
   ↓          ↓          ↓           ↓
 (step)    (step)    (wait)      (step+retry)
```

## 前提条件

- Python 3.13+ または Node.js 22+
- AWS CLI / SAM CLI
- 東京リージョン対応済み

## ファイル一覧

- `app.py` - Lambda 関数コード
- `template.yaml` - SAM テンプレート
- `invoke.sh` - 実行スクリプト

## デプロイ

```bash
# SAM でデプロイ
sam build
sam deploy --guided
```

## 実行

```bash
# 注文を開始
aws lambda invoke \
  --function-name order-processing-durable \
  --payload '{"customer_id": "cust-123", "items": [{"product_id": "prod-001", "price": 1000, "quantity": 2}]}' \
  response.json

# 実行状態の確認
aws lambda list-durable-executions \
  --function-name order-processing-durable

# 承認コールバックの送信
aws lambda send-durable-execution-callback-success \
  --function-name order-processing-durable \
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
