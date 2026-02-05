#

## 変数定義

```
# バケット名を設定（config.py の BUCKET_NAME と同じ形式）
# STUDENT_ID は環境変数から取得、未設定の場合は 'instructor'
STUDENT_ID=${STUDENT_ID:-instructor}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="dev-on-aws-${STUDENT_ID}-${ACCOUNT_ID}"

echo "バケット名: ${BUCKET_NAME}"

# オブジェクトを格納済みのプレフィックス名を指定します。
PREFIX=Dev
```

## プレフィックス無し

```
aws s3 ls s3://${BUCKET_NAME}
```

## プレフィックス有り

```
aws s3 ls s3://${BUCKET_NAME}/${PREFIX}
```
