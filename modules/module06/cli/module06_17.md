#

## 変数定義

```
# 作成済みのバケット名を指定します。
BUCKET_NAME=developing-on-aws-sample
```

## 事前設定

`~/.aws/config` に次の設定を行います。

```
[default]
s3=
  max_concurrent_requests=20
  max_queue_size=10000
  multipart_threshold=100MB
  multipart_chunksize=16MB
```

## このサンプルでは2つのターミナルを使用します。
## 1つめのターミナル：小さな容量のデータを作成して putObjectを実行します。

```
mkdir -p ~/multipart
cd ~/multipart
dd if=/dev/zero of=1MB.img bs=1M count=1
ls -lh

aws s3 cp 1MB.img s3://${BUCKET_NAME}/
```

## 1つめのターミナル：大きな容量のデータを作成して マルチパートアップロードを実行します。

```
mkdir -p ~/multipart
cd ~/multipart
dd if=/dev/zero of=500MB.img bs=1M count=500
ls -lh

aws s3 cp 500MB.img s3://${BUCKET_NAME}/
```

## 2つめのターミナルでマルチパートアップロードを実行したら、すぐに1つめのターミナルで list-multipart-uploads コマンドを実行します。

```
aws s3api list-multipart-uploads --bucket ${BUCKET_NAME}
```

## ファイルの削除

```
aws s3 rm s3://${BUCKET_NAME}/1MB.img
aws s3 rm s3://${BUCKET_NAME}/500MB.img
```
