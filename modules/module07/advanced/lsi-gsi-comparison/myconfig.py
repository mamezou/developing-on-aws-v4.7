# config.py から動的にテーブル名プレフィックスを取得
import sys
import os

# スクリプトのディレクトリを基準にパスを解決（どこから実行しても動作）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
from config import STUDENT_ID

TABLE_NAME = f"Orders-{STUDENT_ID}"
LSI_NAME = "AmountIndex"
GSI_NAME = "ProductIndex"
