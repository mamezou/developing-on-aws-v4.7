# Lambda 関数の呼び出し

作成した Lambda 関数を呼び出します。

## 実行方法

```bash
cd modules/module09/cli
```

## Lambda関数を呼び出す

```bash
aws lambda invoke --function-name ${FUNCTION_NAME} response.txt
cat response.txt
```

## Lambda Functionを削除する

```bash
# aws lambda delete-function --function-name ${FUNCTION_NAME}
```
