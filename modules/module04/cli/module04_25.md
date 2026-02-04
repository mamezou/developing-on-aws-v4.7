# Module 04: AWS CLI プロファイル

## 変数定義

```bash
# バケット名を設定（config.py の BUCKET_NAME と同じ形式）
STUDENT_ID=${STUDENT_ID:-instructor}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="dev-on-aws-${STUDENT_ID}-${ACCOUNT_ID}"

# ~/.aws/config で設定済みの profile 名を指定
PROFILE=staging

echo "バケット名: ${BUCKET_NAME}"
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

