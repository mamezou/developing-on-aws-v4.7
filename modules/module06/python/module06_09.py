"""
Module 06: S3 バケット存在確認

デモ内容:
- head_bucket() を使用したバケット存在確認
- エラーコードによる状態判定（404: 存在しない、403: 他アカウント所有）

実行方法:
  python3 module06_09.py
"""
import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME
import boto3
import botocore

def verifyBucketName(s3Client, bucket):
    try:
        ## バケットが AWS に既に存在するかどうか確認する
        s3Client.head_bucket(Bucket=bucket)
        ## コマンドが成功した場合、バケットはアカウントに既に存在する
        print(f'Bucket "{bucket}" already exists in your account')
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            ## 404 エラーコードを受信した場合、その名前のバケットは
            ##  AWS には存在しない
            print(f'Bucket "{bucket}" not found, you can create it')
        if error_code == 403:
            ## 403 エラーコードを受信した場合、その名前のバケットは 
            ##  別の AWS アカウントに存在する
            print(f'Bucket "{bucket}" is owned by another AWS Account')

if __name__ == "__main__":
    s3Client = boto3.client('s3')
    print(f"Checking bucket: {BUCKET_NAME}")
    verifyBucketName(s3Client, BUCKET_NAME)
