# S3 Range GET

S3 オブジェクトの一部分だけを取得する Range GET を確認します。

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

## Range GET のテスト用テキストファイルを作成してバケットに格納する

```bash
tee abc.txt << EOF
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
EOF

cat abc.txt

aws s3 cp abc.txt s3://${BUCKET_NAME}/
```

## aws cli による Range GET

```bash
aws s3api get-object --bucket ${BUCKET_NAME} --key abc.txt --range bytes=0-19 abc_0-19.txt
cat abc_0-19.txt

aws s3api get-object --bucket ${BUCKET_NAME} --key abc.txt --range bytes=20-39 abc_20-39.txt
cat abc_20-39.txt
```

## 参考 : curlを使用したRange GET
## 事前にバケットポリシーもしくはACLでオブジェクトをパブリックにする必要があります。

```bash
curl https://${BUCKET_NAME}.s3.amazonaws.com/abc.txt / -i -H "Range: bytes=0-19"
curl https://${BUCKET_NAME}.s3.amazonaws.com/abc.txt / -i -H "Range: bytes=20-39"
```

## オブジェクトの削除

```bash
aws s3 rm s3://${BUCKET_NAME}/abc.txt
```
