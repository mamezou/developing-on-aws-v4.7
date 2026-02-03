#

## 変数定義

```
# オブジェクトを格納済みのバケット名を指定します。
BUCKET_NAME=developing-on-aws-sample
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
