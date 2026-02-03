## REST API を呼び出す
REST_API_ID=uirxndwta1
RESOURCE_ID=ybfw2gvpz0

aws apigateway test-invoke-method --rest-api-id ${REST_API_ID} --resource-id ${RESOURCE_ID} --http-method GET --path-with-query-string '/'
