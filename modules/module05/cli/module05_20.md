#

## 変数定義

```
# バケット名を設定（config.py の BUCKET_NAME と同じ形式）
# STUDENT_ID は環境変数から取得、未設定の場合は 'instructor'
STUDENT_ID=${STUDENT_ID:-instructor}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="dev-on-aws-${STUDENT_ID}-${ACCOUNT_ID}"

echo "バケット名: ${BUCKET_NAME}"
```

## リージョン情報の取得

```
aws configure get region
```

## バケット一覧の表示

```
aws s3 ls
```

## バケットの作成

```
aws s3 mb s3://${BUCKET_NAME} --region ap-northeast-1

aws s3 mb s3://${BUCKET_NAME}-us-east-1 --region us-east-1
```

## バケット一覧の取得

```
aws s3api list-buckets --query 'Buckets[].Name'
```

## バケットのリージョン情報取得（us-east-1に作られたバケットはnullが返却される）

```
aws s3api get-bucket-location --bucket ${BUCKET_NAME}

aws s3api get-bucket-location --bucket ${BUCKET_NAME}-us-east-1
```

## バケットの削除

```
aws s3 rb s3://${BUCKET_NAME}

aws s3 rb s3://${BUCKET_NAME}-us-east-1
```
