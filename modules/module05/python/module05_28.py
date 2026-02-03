import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME, REGION
import boto3

# S3リソースを作成する
resource = boto3.resource('s3')
bucket = resource.Bucket(BUCKET_NAME)

print(f"Creating bucket: {BUCKET_NAME}")

bucket.create(
    CreateBucketConfiguration={
        'LocationConstraint': REGION
    }
)

print(f"Bucket created: {BUCKET_NAME}")

# バケット一覧の表示
# aws s3 ls

# バケットの削除
# aws s3 rb s3://{BUCKET_NAME}
#  or
# bucket.delete()
