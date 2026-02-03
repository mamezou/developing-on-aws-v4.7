import boto3

region = 'ap-northeast-1'
bucket_name = 'developing-test-1234'

s3_client = boto3.client('s3', region_name=region)
location = { 'LocationConstraint': region }

s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

# バケットの削除
# s3_client.delete_bucket(Bucket=bucket_name)
