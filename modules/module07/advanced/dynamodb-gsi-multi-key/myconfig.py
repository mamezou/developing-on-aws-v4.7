"""
DynamoDB GSI マルチ属性キー デモ用設定
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from config import STUDENT_ID, REGION

# テーブル名（受講生ごとに一意）
# 従来方式（合成キー）
TABLE_TRADITIONAL = f'Orders-Traditional-{STUDENT_ID}'
# マルチ属性キー方式
TABLE_MULTI_ATTR = f'Orders-MultiAttr-{STUDENT_ID}'

# GSI 名
INDEX_NAME = 'CustomerStatusIndex'

if __name__ == "__main__":
    print(f"Student ID: {STUDENT_ID}")
    print(f"Region: {REGION}")
    print(f"Traditional Table: {TABLE_TRADITIONAL}")
    print(f"Multi-Attr Table: {TABLE_MULTI_ATTR}")
