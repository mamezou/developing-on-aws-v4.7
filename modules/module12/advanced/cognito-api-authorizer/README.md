# Cognito オーソライザー + API Gateway

Cognito ユーザープールで認証し、JWT トークンを使って API Gateway にアクセスするデモです。

## アーキテクチャ

```
ユーザー → Cognito認証 → JWT取得 → API Gateway → Lambda
                              ↓
                    Cognito オーソライザーで検証
```

## 実行方法

```bash
cd modules/module12/advanced/cognito-api-authorizer

# ユニークな識別子を生成
UNIQUE_ID=$(date +%s | tail -c 5)
echo "UNIQUE_ID: ${UNIQUE_ID}"
```

### 1. Cognito ユーザープールの作成

```bash
# ユーザープール作成
aws cognito-idp create-user-pool \
  --pool-name api-auth-pool-${UNIQUE_ID} \
  --auto-verified-attributes email \
  --username-attributes email \
  --policies 'PasswordPolicy={MinimumLength=8,RequireUppercase=false,RequireLowercase=true,RequireNumbers=true,RequireSymbols=false}'

USER_POOL_ID=$(aws cognito-idp list-user-pools --max-results 10 --query "UserPools[?Name=='api-auth-pool-${UNIQUE_ID}'].Id" --output text)
echo "USER_POOL_ID: ${USER_POOL_ID}"

# アプリクライアント作成
aws cognito-idp create-user-pool-client \
  --user-pool-id ${USER_POOL_ID} \
  --client-name api-client-${UNIQUE_ID} \
  --explicit-auth-flows ALLOW_ADMIN_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --no-generate-secret

CLIENT_ID=$(aws cognito-idp list-user-pool-clients --user-pool-id ${USER_POOL_ID} --query "UserPoolClients[0].ClientId" --output text)
echo "CLIENT_ID: ${CLIENT_ID}"
```

### 2. テストユーザーの作成

```bash
aws cognito-idp admin-create-user \
  --user-pool-id ${USER_POOL_ID} \
  --username apiuser@example.com \
  --user-attributes Name=email,Value=apiuser@example.com Name=email_verified,Value=true \
  --message-action SUPPRESS

aws cognito-idp admin-set-user-password \
  --user-pool-id ${USER_POOL_ID} \
  --username apiuser@example.com \
  --password "ApiTest1234" \
  --permanent
```

### 3. Lambda 関数の作成

```bash
# Lambda 用 IAM ロール作成
aws iam create-role \
  --role-name cognito-api-lambda-role-${UNIQUE_ID} \
  --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy \
  --role-name cognito-api-lambda-role-${UNIQUE_ID} \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

sleep 10

LAMBDA_ROLE_ARN=$(aws iam get-role --role-name cognito-api-lambda-role-${UNIQUE_ID} --query 'Role.Arn' --output text)

# Lambda 関数作成
zip function.zip lambda_function.py
# zip がない場合: python3 -c "import zipfile; zipfile.ZipFile('function.zip','w').write('lambda_function.py')"

aws lambda create-function \
  --function-name protected-api-${UNIQUE_ID} \
  --runtime python3.12 \
  --role ${LAMBDA_ROLE_ARN} \
  --handler lambda_function.handler \
  --zip-file fileb://function.zip
```

### 4. API Gateway の作成

```bash
# REST API 作成
aws apigateway create-rest-api \
  --name cognito-protected-api-${UNIQUE_ID} \
  --endpoint-configuration types=REGIONAL

REST_API_ID=$(aws apigateway get-rest-apis --query "items[?name=='cognito-protected-api-${UNIQUE_ID}'].id" --output text)
ROOT_RESOURCE_ID=$(aws apigateway get-resources --rest-api-id ${REST_API_ID} --query "items[?path=='/'].id" --output text)
echo "REST_API_ID: ${REST_API_ID}"

# /secure リソース作成
aws apigateway create-resource \
  --rest-api-id ${REST_API_ID} \
  --parent-id ${ROOT_RESOURCE_ID} \
  --path-part secure

RESOURCE_ID=$(aws apigateway get-resources --rest-api-id ${REST_API_ID} --query "items[?path=='/secure'].id" --output text)
```

### 5. Cognito オーソライザーの作成

```bash
USER_POOL_ARN=$(aws cognito-idp describe-user-pool --user-pool-id ${USER_POOL_ID} --query 'UserPool.Arn' --output text)

aws apigateway create-authorizer \
  --rest-api-id ${REST_API_ID} \
  --name cognito-authorizer \
  --type COGNITO_USER_POOLS \
  --provider-arns ${USER_POOL_ARN} \
  --identity-source 'method.request.header.Authorization'

AUTHORIZER_ID=$(aws apigateway get-authorizers --rest-api-id ${REST_API_ID} --query "items[?name=='cognito-authorizer'].id" --output text)
echo "AUTHORIZER_ID: ${AUTHORIZER_ID}"
```

### 6. メソッドと統合の設定

```bash
REGION=$(aws configure get region)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
LAMBDA_ARN="arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:protected-api-${UNIQUE_ID}"

# GET メソッド作成（Cognito オーソライザー付き）
aws apigateway put-method \
  --rest-api-id ${REST_API_ID} \
  --resource-id ${RESOURCE_ID} \
  --http-method GET \
  --authorization-type COGNITO_USER_POOLS \
  --authorizer-id ${AUTHORIZER_ID}

# Lambda 統合
aws apigateway put-integration \
  --rest-api-id ${REST_API_ID} \
  --resource-id ${RESOURCE_ID} \
  --http-method GET \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/${LAMBDA_ARN}/invocations"

# Lambda 実行権限
aws lambda add-permission \
  --function-name protected-api-${UNIQUE_ID} \
  --statement-id apigateway-invoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:${REGION}:${ACCOUNT_ID}:${REST_API_ID}/*/GET/secure"

# デプロイ
aws apigateway create-deployment \
  --rest-api-id ${REST_API_ID} \
  --stage-name dev

API_URL="https://${REST_API_ID}.execute-api.${REGION}.amazonaws.com/dev/secure"
echo "API_URL: ${API_URL}"
```

### 7. 動作確認

```bash
# トークンなしでアクセス（401 エラー）
curl -s ${API_URL}

# トークンを取得
TOKEN_RESPONSE=$(aws cognito-idp admin-initiate-auth \
  --user-pool-id ${USER_POOL_ID} \
  --client-id ${CLIENT_ID} \
  --auth-flow ADMIN_USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=apiuser@example.com,PASSWORD=ApiTest1234)

ID_TOKEN=$(echo ${TOKEN_RESPONSE} | python3 -c "import sys,json; print(json.load(sys.stdin)['AuthenticationResult']['IdToken'])")

# トークン付きでアクセス（成功）
curl -s -H "Authorization: ${ID_TOKEN}" ${API_URL}
```

### 8. クリーンアップ

```bash
# API Gateway 削除
aws apigateway delete-rest-api --rest-api-id ${REST_API_ID}

# Lambda 削除
aws lambda delete-function --function-name protected-api-${UNIQUE_ID}

# IAM ロール削除
aws iam detach-role-policy \
  --role-name cognito-api-lambda-role-${UNIQUE_ID} \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name cognito-api-lambda-role-${UNIQUE_ID}

# Cognito 削除
aws cognito-idp admin-delete-user --user-pool-id ${USER_POOL_ID} --username apiuser@example.com
aws cognito-idp delete-user-pool-client --user-pool-id ${USER_POOL_ID} --client-id ${CLIENT_ID}
aws cognito-idp delete-user-pool --user-pool-id ${USER_POOL_ID}

rm -f function.zip
```

## ファイル

- `lambda_function.py` - 保護された API のバックエンド
- `trust-policy.json` - Lambda 用 IAM 信頼ポリシー
