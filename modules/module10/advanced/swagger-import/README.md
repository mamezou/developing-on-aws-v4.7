# API Gateway Swagger インポートデモ

OpenAPI (Swagger) 定義から REST API を作成し、テスト呼び出しを行うデモです。

## 実行方法

```bash
cd modules/module10/advanced/swagger-import

# 受講者ごとにユニークな識別子を設定
STUDENT_ID=${STUDENT_ID:-instructor}
echo "STUDENT_ID: ${STUDENT_ID}"
```

### 1. REST API を作成（Swagger インポート）

```bash
# API 名を動的に設定して作成
sed "s/PetStore API/PetStore API ${STUDENT_ID}/" api-definition.yaml > /tmp/api-definition-${STUDENT_ID}.yaml

aws apigateway import-rest-api \
  --body fileb:///tmp/api-definition-${STUDENT_ID}.yaml \
  --fail-on-warnings
```

### 2. API ID を取得

```bash
REST_API_ID=$(aws apigateway get-rest-apis --query "items[?name=='PetStore API ${STUDENT_ID}'].id" --output text)
echo "REST_API_ID: ${REST_API_ID}"
```

### 3. リソース ID を取得

```bash
# /pets リソースの ID を取得
RESOURCE_ID=$(aws apigateway get-resources --rest-api-id ${REST_API_ID} --query "items[?path=='/pets'].id" --output text)
echo "RESOURCE_ID: ${RESOURCE_ID}"
```

### 4. テスト呼び出し

```bash
aws apigateway test-invoke-method \
  --rest-api-id ${REST_API_ID} \
  --resource-id ${RESOURCE_ID} \
  --http-method GET \
  --path-with-query-string '/pets'
```

### 5. デプロイ

```bash
aws apigateway create-deployment \
  --rest-api-id ${REST_API_ID} \
  --stage-name dev

# エンドポイント URL
echo "https://${REST_API_ID}.execute-api.$(aws configure get region).amazonaws.com/dev/pets"
```

### 6. クリーンアップ

```bash
aws apigateway delete-rest-api --rest-api-id ${REST_API_ID}
```

## ファイル

- `api-definition.yaml` - OpenAPI (Swagger) 定義
