import sys
sys.path.insert(0, '../../../')
from config import BUCKET_NAME
import boto3

def listClient():
    s3client = boto3.client('s3')
    response = s3client.list_objects_v2(Bucket=BUCKET_NAME)
    for content in response['Contents']:
        print(content['Key'], content['LastModified'])

def listResource():
    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket(BUCKET_NAME)
    for object in bucket.objects.all():
        print(object.key, object.last_modified)

if __name__ == "__main__": 
    listClient()
    # listResource()
