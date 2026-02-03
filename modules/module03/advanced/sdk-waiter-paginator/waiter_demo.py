"""
EC2 Waiter デモ

EC2 インスタンスを起動して、running 状態になるまで待機します。
SDK の Waiter を使うことで、手動ポーリングが不要になります。
"""

import boto3
import time
import sys
sys.path.insert(0, '../../../../')
from config import REGION

ec2_client = boto3.client('ec2', region_name=REGION)

def get_latest_ami():
    """最新の Amazon Linux 2023 AMI を取得"""
    response = ec2_client.describe_images(
        Owners=['amazon'],
        Filters=[
            {'Name': 'name', 'Values': ['al2023-ami-2023*-x86_64']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return images[0]['ImageId'] if images else None


def main():
    # 最新の AMI を取得
    ami_id = get_latest_ami()
    if not ami_id:
        print("❌ AMI が見つかりません")
        return
    
    print(f"使用する AMI: {ami_id}")
    
    # インスタンス起動
    print("\n=== EC2 インスタンスを起動 ===")
    response = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType='t3.micro',
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'WaiterDemo'}]
        }]
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    print(f"インスタンス ID: {instance_id}")
    print("状態: pending")
    
    # Waiter で待機
    print("\n=== Waiter で running 状態まで待機 ===")
    start_time = time.time()
    
    waiter = ec2_client.get_waiter('instance_running')
    print("待機中...")
    waiter.wait(InstanceIds=[instance_id])
    
    elapsed = time.time() - start_time
    print(f"✅ インスタンスが起動しました（{elapsed:.1f}秒）")
    
    # 状態確認
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    print(f"現在の状態: {state}")
    
    # クリーンアップ
    print("\n=== クリーンアップ ===")
    ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(f"インスタンス {instance_id} を終了しました")
    
    # 利用可能な Waiter 一覧
    print("\n=== 利用可能な EC2 Waiter ===")
    for name in ec2_client.waiter_names:
        print(f"  - {name}")


if __name__ == '__main__':
    main()
