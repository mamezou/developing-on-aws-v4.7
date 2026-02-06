"""
S3 Paginator デモ

S3 バケット内の大量オブジェクト一覧を取得します。
SDK の Paginator を使うことで、NextToken の管理が不要になります。
"""

import boto3
import sys
import os

# スクリプトのディレクトリを基準にパスを解決（どこから実行しても動作）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
from config import BUCKET_NAME, REGION

s3_client = boto3.client('s3', region_name=REGION)

PREFIX = 'paginator-demo/'


def demo_manual_paging():
    """手動ページング（非推奨）"""
    print("=== 手動ページング（非推奨）===")
    print("NextToken を自分で管理する必要があります\n")
    
    objects = []
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    objects.extend(response.get('Contents', []))
    page_count = 1
    
    while response.get('IsTruncated'):
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=PREFIX,
            ContinuationToken=response['NextContinuationToken']
        )
        objects.extend(response.get('Contents', []))
        page_count += 1
    
    print(f"ページ数: {page_count}")
    print(f"オブジェクト数: {len(objects)}")
    return len(objects)


def demo_paginator():
    """Paginator 使用（推奨）"""
    print("\n=== Paginator 使用（推奨）===")
    print("NextToken の管理が不要です\n")
    
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET_NAME, Prefix=PREFIX)
    
    total_count = 0
    total_size = 0
    page_count = 0
    
    for page in page_iterator:
        contents = page.get('Contents', [])
        page_count += 1
        total_count += len(contents)
        
        for obj in contents:
            total_size += obj['Size']
        
        print(f"  ページ {page_count}: {len(contents)} オブジェクト")
    
    print(f"\n✅ 合計: {total_count} オブジェクト ({total_size / 1024:.2f} KB)")
    return total_count


def main():
    print(f"バケット: {BUCKET_NAME}")
    print(f"プレフィックス: {PREFIX}\n")
    
    # 手動ページング
    manual_count = demo_manual_paging()
    
    # Paginator
    paginator_count = demo_paginator()
    
    # 比較
    print("\n=== 比較 ===")
    print(f"手動ページング: {manual_count} オブジェクト")
    print(f"Paginator: {paginator_count} オブジェクト")
    
    # 利用可能な Paginator 一覧（一部）
    print("\n=== S3 で利用可能な Paginator（一部）===")
    paginators = ['list_objects_v2', 'list_buckets', 'list_object_versions', 'list_parts']
    for name in paginators:
        print(f"  - {name}")


if __name__ == '__main__':
    main()
