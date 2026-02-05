"""
Movies サンプル用設定

共通の config.py から STUDENT_ID, REGION を取得し、一意のテーブル名を生成します。
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

from config import STUDENT_ID, REGION

# テーブル名（受講生ごとに一意）
TABLE_NAME = f'Movies-{STUDENT_ID}'

if __name__ == "__main__":
    print(f"Table Name: {TABLE_NAME}")
    print(f"Region: {REGION}")
