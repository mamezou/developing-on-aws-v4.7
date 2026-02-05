# S3 オブジェクト一覧表示

S3 バケット内のオブジェクト一覧を表示します。

## 実行方法

```bash
cd modules/module05/cli
```

## 変数定義

```bash
STUDENT_ID=${STUDENT_ID:-instructor}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="dev-on-aws-${STUDENT_ID}-${ACCOUNT_ID}"

echo "バケット名: ${BUCKET_NAME}"

# オブジェクトを格納済みのプレフィックス名を指定します。
PREFIX=Dev
```

## プレフィックス無し

```bash
aws s3 ls s3://${BUCKET_NAME}
```

## プレフィックス有り

```bash
aws s3 ls s3://${BUCKET_NAME}/${PREFIX}
```
