# X-Ray トレーシングデモ

SAM で Lambda + API Gateway をデプロイし、X-Ray でリクエストをトレースするデモです。

## アーキテクチャ

```
クライアント → API Gateway → Lambda → DynamoDB
                  ↓              ↓         ↓
              X-Ray トレース（サービスマップで可視化）
```

## 前提条件

```bash
# Python バージョンを確認（3.9 が必要）
python3 --version

# SAM CLI がインストールされていることを確認
sam --version
```

## 実行方法

```bash
cd modules/module14/advanced/xray-tracing

# 受講者ごとにユニークな識別子を設定
STUDENT_ID=${STUDENT_ID:-instructor}
STACK_NAME="xray-demo-${STUDENT_ID}"
echo "STACK_NAME: ${STACK_NAME}"
```

### 1. SAM でデプロイ

```bash
sam build
```

※ EC2 環境には Docker がないため `--use-container` は使用不可

```bash
sam deploy --guided
```

対話形式で入力（※ 変数展開されないので、上記で確認した値を手入力）：
- Stack Name → `xray-demo-${STUDENT_ID}`（例: `xray-demo-instructor`）
- AWS Region → `ap-northeast-1`
- Confirm changes before deploy → `N`
- Allow SAM CLI IAM role creation → `Y`
- Disable rollback → `N`
- TracedFunction may not have authorization defined, Is this okay? → `Y`
- Save arguments to configuration file → `Y`

### 2. API を呼び出してトレースを生成

```bash
# API エンドポイントを取得
API_URL=$(aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" \
  --output text)

echo "API_URL: ${API_URL}"

# 複数回呼び出してトレースデータを生成
for i in {1..5}; do
  curl -s ${API_URL}
  echo ""
  sleep 1
done
```

### 3. X-Ray でトレースを確認

```bash
# 過去5分間のトレースサマリーを取得
START_TIME=$(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%SZ)
END_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)

aws xray get-trace-summaries \
  --start-time ${START_TIME} \
  --end-time ${END_TIME} \
  --query "TraceSummaries[].{Id:Id,Duration:Duration,ResponseTime:ResponseTime}"
```

### 4. サービスマップを取得

```bash
aws xray get-service-graph \
  --start-time ${START_TIME} \
  --end-time ${END_TIME} \
  --query "Services[].{Name:Name,Type:Type}"
```

### 5. マネジメントコンソールで確認

AWS コンソール → X-Ray → サービスマップ で視覚的に確認できます。

### 6. クリーンアップ

```bash
sam delete --stack-name ${STACK_NAME} --no-prompts
```

## ファイル

- `template.yaml` - SAM テンプレート（X-Ray 有効化）
- `app.py` - Lambda 関数（X-Ray SDK でサブセグメント作成）

## X-Ray の主要概念

- **トレース**: 1つのリクエストの全体像
- **セグメント**: サービス単位の処理（API Gateway, Lambda など）
- **サブセグメント**: セグメント内の詳細（外部 API 呼び出し、DB クエリなど）
- **アノテーション**: 検索可能なメタデータ
- **メタデータ**: 検索不可の追加情報

## 参考リンク

- [X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)
- [X-Ray SDK for Python](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python.html)
