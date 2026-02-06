# Lambda 関数の作成

AWS CLI で Lambda 関数を作成・デプロイします。

## 実行方法

```bash
cd modules/module09/cli
```

## Lambdaの関数をzip化する

```bash
zip ./function.zip app.py
```

## 変数定義

```bash
STUDENT_ID=${STUDENT_ID:-instructor}
ROLE_NAME="lambda-hello-${STUDENT_ID}-role"
FUNCTION_NAME="PythonHelloWorld-${STUDENT_ID}"
echo "ROLE_NAME: ${ROLE_NAME}"
echo "FUNCTION_NAME: ${FUNCTION_NAME}"
```

## IAM Roleを作成する

```bash
aws iam create-role --role-name ${ROLE_NAME} --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
ROLE_ARN=$(aws iam get-role --role-name ${ROLE_NAME} --query Role.Arn --output text)

# IAM ロールの伝播を待機
sleep 10
```

## Lambda Functionを作成する

```bash
aws lambda create-function --function-name ${FUNCTION_NAME} --handler app.lambda_handler --runtime python3.9 --role ${ROLE_ARN} --environment Variables={MESSAGE="Hello Lambda."} --zip-file fileb://function.zip
```

## Lambda Functionを削除する

```bash
aws lambda delete-function --function-name ${FUNCTION_NAME}
```

## IAM Roleを削除する

```bash
aws iam detach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name ${ROLE_NAME}
```
