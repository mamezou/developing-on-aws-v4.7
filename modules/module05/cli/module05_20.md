#

## 変数定義

```
# 一意な任意のバケット名を指定します。
BUCKET_NAME=developing-on-aws-sample
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
