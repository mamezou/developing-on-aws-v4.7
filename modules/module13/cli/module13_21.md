## SAM CLIのインストール
## https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html#install-sam-cli-instructions

```
cd ~
curl -LO https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
sam --version
```

## SAM Hello World!
## https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html
## SAMプロジェクトの初期化

```
sam init

Which template source would you like to use? 1
Choose an AWS Quick Start application template 1
Use the most popular runtime and package type? (Python and zip) [y/N]: Y
Would you like to enable X-Ray tracing on the function(s) in your application?  [y/N]: N
Would you like to enable monitoring using CloudWatch Application Insights? N
Project name [sam-app]: sam-app

cd sam-app
```

## テンプレートファイルの確認

```
cat template.yaml
```

## 外部モジュールのダウンロード

```
sam build --use-container
```

## ローカルでのテスト
sam local invoke HelloWorldFunction 2>/dev/null

## デプロイ作業

```
sam deploy --guided

Stack Name [sam-app]:
AWS Region [ap-northeast-1]:
Confirm changes before deploy [y/N]: 
Allow SAM CLI IAM role creation [Y/n]:
Disable rollback [y/N]: 
HelloWorldFunction may not have authorization defined, Is this okay? [y/N]: Y
Save arguments to configuration file [Y/n]:
SAM configuration file [samconfig.toml]:
SAM configuration environment [default]: 
```

## リソースの削除

```
sam delete
```
