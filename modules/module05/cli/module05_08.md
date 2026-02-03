#

## 変数定義

```
# オブジェクトを格納済みのバケット名を指定します。
BUCKET_NAME=developing-on-aws-sample

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
