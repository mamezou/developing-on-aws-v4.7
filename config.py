"""
Developing on AWS トレーニング用 共通設定

このファイルは各デモスクリプトで使用するリソース名を動的に生成します。
受講生ごとに一意のリソース名が生成されるため、同一アカウント内での競合を防ぎます。
"""
import os
import boto3

def get_account_id():
    """AWS アカウント ID を取得"""
    sts = boto3.client('sts')
    return sts.get_caller_identity()['Account']

def get_student_id():
    """
    受講生 ID を取得
    - EC2 環境: CDK で設定された STUDENT_ID 環境変数を使用
    - ローカル環境: デフォルト値 'instructor' を使用
    """
    return os.environ.get('STUDENT_ID', 'instructor')

# 動的に生成されるリソース名
STUDENT_ID = get_student_id()
ACCOUNT_ID = get_account_id()

# S3 バケット名（グローバルで一意）
BUCKET_NAME = f"dev-on-aws-{STUDENT_ID}-{ACCOUNT_ID}"

# DynamoDB テーブル名
TABLE_NAME = f"dev-on-aws-{STUDENT_ID}-demo"

# リージョン
REGION = os.environ.get('AWS_DEFAULT_REGION', 'ap-northeast-1')

if __name__ == "__main__":
    print(f"Student ID: {STUDENT_ID}")
    print(f"Account ID: {ACCOUNT_ID}")
    print(f"Bucket Name: {BUCKET_NAME}")
    print(f"Table Name: {TABLE_NAME}")
    print(f"Region: {REGION}")
