import boto3

region = 'ap-northeast-1'
bucket_name = 'developing-test-12345'

s3_client = boto3.client('s3', region_name=region)
location = { 'LocationConstraint': region }

s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

print('バケットの作成をリクエストしました')

waiter = s3_client.get_waiter('bucket_exists')
waiter.wait(Bucket=bucket_name)

print('バケットの作成が完了しました')

# バケットの削除
# s3_client.delete_bucket(Bucket=bucket_name)
