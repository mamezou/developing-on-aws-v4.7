# Cognito ユーザープール基本操作

ユーザープール作成 → ユーザー登録 → 認証 → JWT トークン取得までの流れを CLI で確認します。

## 実行方法

```bash
cd modules/module12/cli

# ユニークな識別子を生成（受講者ごとに異なる値）
UNIQUE_ID=$(date +%s | tail -c 5)
echo "UNIQUE_ID: ${UNIQUE_ID}"
```

### 1. ユーザープールの作成

```bash
aws cognito-idp create-user-pool \
  --pool-name demo-user-pool-${UNIQUE_ID} \
  --auto-verified-attributes email \
  --username-attributes email \
  --policies 'PasswordPolicy={MinimumLength=8,RequireUppercase=false,RequireLowercase=true,RequireNumbers=true,RequireSymbols=false}'

# ユーザープール ID を取得
USER_POOL_ID=$(aws cognito-idp list-user-pools --max-results 10 --query "UserPools[?Name=='demo-user-pool-${UNIQUE_ID}'].Id" --output text)
echo "USER_POOL_ID: ${USER_POOL_ID}"
```

### 2. アプリクライアントの作成

```bash
aws cognito-idp create-user-pool-client \
  --user-pool-id ${USER_POOL_ID} \
  --client-name demo-app-client-${UNIQUE_ID} \
  --explicit-auth-flows ALLOW_ADMIN_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --no-generate-secret

# クライアント ID を取得
CLIENT_ID=$(aws cognito-idp list-user-pool-clients --user-pool-id ${USER_POOL_ID} --query "UserPoolClients[?ClientName=='demo-app-client-${UNIQUE_ID}'].ClientId" --output text)
echo "CLIENT_ID: ${CLIENT_ID}"
```

### 3. ユーザーの作成

```bash
# 管理者としてユーザーを作成（メール確認をスキップ）
aws cognito-idp admin-create-user \
  --user-pool-id ${USER_POOL_ID} \
  --username testuser@example.com \
  --user-attributes Name=email,Value=testuser@example.com Name=email_verified,Value=true \
  --message-action SUPPRESS

# パスワードを設定（FORCE_CHANGE_PASSWORD 状態を解除）
aws cognito-idp admin-set-user-password \
  --user-pool-id ${USER_POOL_ID} \
  --username testuser@example.com \
  --password "Test1234" \
  --permanent
```

### 4. 認証してトークンを取得

```bash
aws cognito-idp admin-initiate-auth \
  --user-pool-id ${USER_POOL_ID} \
  --client-id ${CLIENT_ID} \
  --auth-flow ADMIN_USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=testuser@example.com,PASSWORD=Test1234
```

レスポンスに `IdToken`, `AccessToken`, `RefreshToken` が含まれます。

### 5. JWT トークンをデコード

```bash
# IdToken をデコード（ペイロード部分を base64 デコード）
ID_TOKEN="<上記で取得した IdToken>"
echo ${ID_TOKEN} | cut -d'.' -f2 | base64 -d 2>/dev/null | python3 -m json.tool
```

トークンには以下の情報が含まれます：
- `sub`: ユーザーの一意識別子
- `email`: メールアドレス
- `cognito:username`: ユーザー名
- `exp`: 有効期限

### 6. クリーンアップ

```bash
# ユーザーを削除
aws cognito-idp admin-delete-user \
  --user-pool-id ${USER_POOL_ID} \
  --username testuser@example.com

# アプリクライアントを削除
aws cognito-idp delete-user-pool-client \
  --user-pool-id ${USER_POOL_ID} \
  --client-id ${CLIENT_ID}

# ユーザープールを削除
aws cognito-idp delete-user-pool \
  --user-pool-id ${USER_POOL_ID}
```
