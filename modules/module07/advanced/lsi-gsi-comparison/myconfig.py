# config.py から動的にテーブル名プレフィックスを取得
import sys
sys.path.insert(0, '../../../../')
from config import STUDENT_ID

TABLE_NAME = f"Orders-{STUDENT_ID}"
LSI_NAME = "AmountIndex"
GSI_NAME = "ProductIndex"
