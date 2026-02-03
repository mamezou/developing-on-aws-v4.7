#

## 変数定義

```
# 作成済みのバケット名を指定します。
BUCKET_NAME=developing-on-aws-sample
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
