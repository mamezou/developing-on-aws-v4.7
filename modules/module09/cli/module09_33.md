## Lambdaの関数をzip化する
zip ./function.zip app.py

## IAM Roleを作成する
aws iam create-role --role-name lambda-hello-world --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name lambda-hello-world --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
ROLE_ARN=`aws iam get-role --role-name lambda-hello-world --query Role.Arn --output text`

## Lambda Functionを作成する
aws lambda create-function --function-name PythonHelloWorld --handler app.lambda_handler --runtime python3.7 --role ${ROLE_ARN} --environment Variables={MESSAGE="Hello Lambda."} --zip-file fileb://function.zip

## Lambda Functionを削除する
aws lambda delete-function --function-name PythonHelloWorld

## IAM Roleを削除する
aws iam detach-role-policy --role-name lambda-hello-world --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name lambda-hello-world
