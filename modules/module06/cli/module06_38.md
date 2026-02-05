# S3 静的ウェブサイトホスティング

S3 で静的ウェブサイトをホストします。

## 実行方法

```bash
cd modules/module06/cli
```

## バケットを作る

```bash
STUDENT_ID=${STUDENT_ID:-instructor}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="dev-on-aws-${STUDENT_ID}-${ACCOUNT_ID}"

echo "バケット名: ${BUCKET_NAME}"
REGION=ap-northeast-1
aws s3 mb s3://${BUCKET_NAME} --region ${REGION}
```

## アクセスコントロールの設定を行う

```bash
aws s3api put-public-access-block --bucket ${BUCKET_NAME} --public-access-block-configuration '{ "BlockPublicAcls": false, "IgnorePublicAcls": false, "BlockPublicPolicy": false, "RestrictPublicBuckets": false }'

aws s3api get-public-access-block --bucket ${BUCKET_NAME}

aws s3api put-bucket-policy --bucket ${BUCKET_NAME} --policy "{\"Version\": \"2012-10-17\", \"Statement\": [{ \"Effect\": \"Allow\", \"Principal\": \"*\", \"Action\": \"s3:GetObject\", \"Resource\": \"arn:aws:s3:::${BUCKET_NAME}/*\" }]}"
```

## 静的ウェブサイトホスティング機能を有効化する

```bash
aws s3 website s3://${BUCKET_NAME} --index-document index.html --error-document error.html
```

## ウェブコンテンツを生成して格納する（ここではSSGとしてJekyllを使用する）
## 事前に[Jekyllのインストールガイド](http://jekyllrb-ja.github.io/docs/installation/)に従ってjekyllコマンドをインストールして下さい。

```bash
rm -rf ~/developing_on_aws_static_site

# Jekyllのプロジェクトを作成します。
(cd ~/ && jekyll new developing_on_aws_static_site)

# サイトのタイトルを変更します。
sed -ie "s/Your awesome title/Hello AWS Developer/" ~/developing_on_aws_static_site/_config.yml

# Jekyllの静的サイトをビルドします。
(cd ~/developing_on_aws_static_site && jekyll build)

# 静的サイトのコンテンツをS3バケットへ同期します。
aws s3 sync ~/developing_on_aws_static_site/_site s3://${BUCKET_NAME}
```

## 静的ウェブサイトホスティングのURLを取得します。
## ※ 出力結果のアドレスにブラウザで接続します。

```bash
echo http://${BUCKET_NAME}.s3-website-${REGION}.amazonaws.com
```

## バケットの削除

```bash
aws s3 rb s3://${BUCKET_NAME} --force
```
