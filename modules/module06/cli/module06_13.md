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

## スケルトンの取得

```
aws s3api get-bucket-versioning --bucket ${BUCKET_NAME} --generate-cli-skeleton output
```

## バージョニング機能の設定状況確認

```
aws s3api get-bucket-versioning --bucket ${BUCKET_NAME}
```

## バージョニング機能の有効化（テキストのサンプルは誤りがあるため注意）

```
aws s3api put-bucket-versioning --bucket ${BUCKET_NAME} --versioning-configuration=Status=Enabled
```

## バージョニング機能の設定状況確認

```
aws s3api get-bucket-versioning --bucket ${BUCKET_NAME}
```
