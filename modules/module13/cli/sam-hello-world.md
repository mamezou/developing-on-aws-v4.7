# SAM Hello World

AWS SAM を使ってサーバーレスアプリケーションをデプロイするデモです。

## SAM CLI のインストール

```bash
cd ~
curl -LO https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
sam --version
```

参考: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

## SAM プロジェクトの初期化

```bash
# 受講者ごとにユニークな識別子を設定
STUDENT_ID=${STUDENT_ID:-instructor}
PROJECT_NAME="sam-app-${STUDENT_ID}"
echo "PROJECT_NAME: ${PROJECT_NAME}"

sam init
```

対話形式で以下を選択：
- Which template source would you like to use? → `1` (AWS Quick Start Templates)
- Choose an AWS Quick Start application template → `1` (Hello World Example)
- Use the most popular runtime and package type? (Python and zip) → `Y`
- Would you like to enable X-Ray tracing? → `N`
- Would you like to enable monitoring using CloudWatch Application Insights? → `N`
- Project name → `sam-app-${STUDENT_ID}`（上記で設定した値を入力）

```bash
cd ${PROJECT_NAME}
```

## テンプレートファイルの確認

```bash
cat template.yaml
```

ポイント：
- `Transform: AWS::Serverless-2016-10-31` で SAM テンプレートを宣言
- `AWS::Serverless::Function` で Lambda + API Gateway を自動構成

## ビルド

```bash
# Docker がある場合（推奨）
sam build --use-container

# Docker がない場合
sam build
```

## ローカルテスト（Docker 必須）

```bash
sam local invoke HelloWorldFunction
```

## デプロイ

```bash
sam deploy --guided
```

対話形式で以下を入力：
- Stack Name → `sam-app-${STUDENT_ID}`（プロジェクト名と同じ）
- AWS Region → `ap-northeast-1`
- Confirm changes before deploy → `N`
- Allow SAM CLI IAM role creation → `Y`
- Disable rollback → `N`
- HelloWorldFunction may not have authorization defined, Is this okay? → `Y`
- Save arguments to configuration file → `Y`
- SAM configuration file → `samconfig.toml`
- SAM configuration environment → `default`

デプロイ完了後、出力された API エンドポイントにアクセスして動作確認。

## クリーンアップ

```bash
sam delete
```

## 参考リンク

- [SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/)
- [SAM CLI Command Reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
