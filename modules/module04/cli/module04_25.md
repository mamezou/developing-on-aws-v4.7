# 

## 変数定義

```
# 一意な任意のバケット名を指定します。
BUCKET_NAME=developing-on-aws-sample-`date +"%Y%m%d"`

# ~/.aws/configで設定済みのprofile名を指定します。
PROFILE=staging
```

## デフォルトプロファイルを使用したコマンド
### バケット一覧の表示

```
aws s3 ls
```

### バケットの作成

```
aws s3 mb s3://${BUCKET_NAME}
```

### 片付け：バケットの削除

```
aws s3 rb s3://${BUCKET_NAME}
```

## プロファイルを使用したコマンド [--profile common]
### バケット一覧の表示

```
aws s3 ls --profile ${PROFILE}
```

### バケットの作成

```
aws s3 mb s3://${BUCKET_NAME} --profile ${PROFILE}
```

### 片付け：バケットの削除

```
aws s3 rb s3://${BUCKET_NAME} --profile ${PROFILE}
```

