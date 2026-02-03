import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME, REGION
import boto3

s3_client = boto3.client('s3', region_name=REGION)
location = { 'LocationConstraint': REGION }

print(f'バケット {BUCKET_NAME} の作成をリクエストします')
s3_client.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration=location)

print('バケットの作成をリクエストしました')

waiter = s3_client.get_waiter('bucket_exists')
waiter.wait(Bucket=BUCKET_NAME)

print('バケットの作成が完了しました')

# バケットの削除
# s3_client.delete_bucket(Bucket=BUCKET_NAME)
