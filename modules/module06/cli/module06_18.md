# 

## 変数定義

```
# 作成済みのバケット名を指定します。
BUCKET_NAME=developing-on-aws-sample
```

## Range GET のテスト用テキストファイルを作成してバケットに格納する

tee abc.txt << EOF
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
EOF

cat abc.txt

aws s3 cp abc.txt s3://${BUCKET_NAME}/

## aws cli による Range GET

```
aws s3api get-object --bucket ${BUCKET_NAME} --key abc.txt --range bytes=0-19 abc_0-19.txt
cat abc_0-19.txt

aws s3api get-object --bucket ${BUCKET_NAME} --key abc.txt --range bytes=20-39 abc_20-39.txt
cat abc_20-39.txt
```

## 参考 : curlを使用したRange GET
## 事前にバケットポリシーもしくはACLでオブジェクトをパブリックにする必要があります。

```
curl https://${BUCKET_NAME}.s3.amazonaws.com/abc.txt / -i -H "Range: bytes=0-19"
curl https://${BUCKET_NAME}.s3.amazonaws.com/abc.txt / -i -H "Range: bytes=20-39"
```

## オブジェクトの削除

```
aws s3 rm s3://${BUCKET_NAME}/abc.txt
```
