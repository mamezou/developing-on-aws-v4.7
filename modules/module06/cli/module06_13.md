# S3 バージョニング設定

S3 バケットのバージョニング機能を有効化します。

## 実行方法

```bash
cd modules/module06/cli
```

## 変数定義

```bash
STUDENT_ID=${STUDENT_ID:-instructor}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="dev-on-aws-${STUDENT_ID}-${ACCOUNT_ID}"

echo "バケット名: ${BUCKET_NAME}"
```

## スケルトンの取得

```bash
aws s3api get-bucket-versioning --bucket ${BUCKET_NAME} --generate-cli-skeleton output
```

## バージョニング機能の設定状況確認

```bash
aws s3api get-bucket-versioning --bucket ${BUCKET_NAME}
```

## バージョニング機能の有効化（テキストのサンプルは誤りがあるため注意）

```bash
aws s3api put-bucket-versioning --bucket ${BUCKET_NAME} --versioning-configuration=Status=Enabled
```

## バージョニング機能の設定状況確認

```bash
aws s3api get-bucket-versioning --bucket ${BUCKET_NAME}
```
