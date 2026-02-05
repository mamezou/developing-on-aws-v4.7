"""
Lambda Durable Functions デプロイスクリプト

AWS CLI 2.33.x では --durable-function-configuration がまだサポートされていないため、
boto3 を使用して Durable Functions を有効化した Lambda 関数を作成します。
"""
import boto3
import zipfile
import os

# 環境変数から取得（デフォルト値あり）
FUNCTION_NAME = os.environ.get('FUNCTION_NAME', 'order-processing-durable')
ROLE_NAME = os.environ.get('ROLE_NAME', 'lambda-durable-demo-role')


def create_deployment_package():
    """app.py を ZIP 化"""
    with zipfile.ZipFile('function.zip', 'w') as zf:
        zf.write('app.py')
    print('Created function.zip')


def deploy_function():
    """Lambda 関数を作成（Durable Functions 有効化）"""
    client = boto3.client('lambda')
    iam = boto3.client('iam')
    
    # ロール ARN を取得
    role = iam.get_role(RoleName=ROLE_NAME)
    role_arn = role['Role']['Arn']
    
    # ZIP ファイルを読み込み
    with open('function.zip', 'rb') as f:
        zip_content = f.read()
    
    # Lambda 関数を作成
    response = client.create_function(
        FunctionName=FUNCTION_NAME,
        Runtime='python3.13',
        Role=role_arn,
        Handler='app.handler',
        Code={'ZipFile': zip_content},
        Timeout=900,
        DurableConfig={
            'ExecutionTimeout': 3600,
            'RetentionPeriodInDays': 7
        }
    )
    print(f"Function ARN: {response['FunctionArn']}")
    
    # バージョンを発行（Durable Functions は修飾された ARN が必要）
    version = client.publish_version(FunctionName=FUNCTION_NAME)
    print(f"Published version: {version['Version']}")
    
    return response


if __name__ == '__main__':
    create_deployment_package()
    deploy_function()
