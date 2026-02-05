# CloudWatch Logs で Lambda ログを確認

Lambda 関数のログを CloudWatch Logs で確認するデモです。

## 前提

Lambda 関数がデプロイ済みであること（Module8 のラボなど）

## ログの確認

### 1. ロググループの一覧

```bash
# Lambda 関数のロググループを検索
aws logs describe-log-groups \
  --log-group-name-prefix "/aws/lambda/" \
  --query "logGroups[].logGroupName"
```

### 2. ログストリームの一覧

```bash
LOG_GROUP="/aws/lambda/<関数名>"

aws logs describe-log-streams \
  --log-group-name ${LOG_GROUP} \
  --order-by LastEventTime \
  --descending \
  --limit 5 \
  --query "logStreams[].logStreamName"
```

### 3. 最新のログを取得

```bash
LOG_GROUP="/aws/lambda/<関数名>"

# 最新のログストリームを取得
STREAM=$(aws logs describe-log-streams \
  --log-group-name ${LOG_GROUP} \
  --order-by LastEventTime \
  --descending \
  --limit 1 \
  --query "logStreams[0].logStreamName" \
  --output text)

# ログイベントを取得
aws logs get-log-events \
  --log-group-name ${LOG_GROUP} \
  --log-stream-name ${STREAM} \
  --limit 20 \
  --query "events[].message" \
  --output text
```

### 4. ログをフィルタリング

```bash
LOG_GROUP="/aws/lambda/<関数名>"

# エラーを含むログを検索
aws logs filter-log-events \
  --log-group-name ${LOG_GROUP} \
  --filter-pattern "ERROR" \
  --limit 10 \
  --query "events[].message"

# 特定の時間範囲で検索（過去1時間）
START_TIME=$(($(date +%s) - 3600))000
aws logs filter-log-events \
  --log-group-name ${LOG_GROUP} \
  --start-time ${START_TIME} \
  --limit 20 \
  --query "events[].message"
```

### 5. ログのリアルタイム監視（tail）

```bash
LOG_GROUP="/aws/lambda/<関数名>"

aws logs tail ${LOG_GROUP} --follow
```

## CloudWatch メトリクス

### Lambda 関数のメトリクス確認

```bash
FUNCTION_NAME="<関数名>"

# 呼び出し回数（過去1時間）
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=${FUNCTION_NAME} \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Sum

# エラー数
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=${FUNCTION_NAME} \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Sum

# 実行時間
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=${FUNCTION_NAME} \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average
```

## 参考リンク

- [CloudWatch Logs CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/logs/)
- [CloudWatch Metrics CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/)
