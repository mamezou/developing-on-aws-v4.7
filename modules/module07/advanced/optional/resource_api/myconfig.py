"""
DynamoDB Resource API サンプル用設定

共通の config.py から STUDENT_ID, REGION を取得し、一意のテーブル名を生成します。
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from config import STUDENT_ID, REGION

# テーブル名（受講生ごとに一意）
TRAINING_TABLE = f'Training-{STUDENT_ID}'
TRAINING_QUERY_SCAN_TABLE = f'TrainingForQueryScan-{STUDENT_ID}'
LIMIT_TEST_TABLE = f'LimitTest-{STUDENT_ID}'

if __name__ == "__main__":
    print(f"Training Table: {TRAINING_TABLE}")
    print(f"Training Query Scan Table: {TRAINING_QUERY_SCAN_TABLE}")
    print(f"Limit Test Table: {LIMIT_TEST_TABLE}")
    print(f"Region: {REGION}")
