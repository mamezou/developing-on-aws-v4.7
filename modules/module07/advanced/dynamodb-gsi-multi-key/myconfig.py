"""
DynamoDB GSI マルチ属性キー デモ用設定

共通の config.py から STUDENT_ID を取得し、一意のテーブル名を生成します。
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from config import STUDENT_ID, REGION

# テーブル名（受講生ごとに一意）
TABLE_NAME = f'Orders-GSI-Demo-{STUDENT_ID}'
INDEX_NAME = 'CustomerStatusIndex'

if __name__ == "__main__":
    print(f"Table Name: {TABLE_NAME}")
    print(f"Index Name: {INDEX_NAME}")
    print(f"Region: {REGION}")
