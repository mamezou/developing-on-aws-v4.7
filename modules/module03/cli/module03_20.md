# AWS CLI - S3 操作

S3 バケットに対する基本的な CLI 操作を確認します。

## 実行方法

```bash
cd modules/module03/cli
```

## 変数定義

```bash
# バケット名を設定（config.py の BUCKET_NAME と同じ形式）
STUDENT_ID=${STUDENT_ID:-instructor}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="dev-on-aws-${STUDENT_ID}-${ACCOUNT_ID}"

echo "バケット名: ${BUCKET_NAME}"
```

## オブジェクトの一覧表示

```
aws s3 ls s3://${BUCKET_NAME} --recursive
```

## オブジェクトのコピー

```
echo `date` > myFile.txt
aws s3 cp myFile.txt s3://${BUCKET_NAME}
```

## ヘルプ

```
aws help
aws s3 help
aws s3 ls help
```
