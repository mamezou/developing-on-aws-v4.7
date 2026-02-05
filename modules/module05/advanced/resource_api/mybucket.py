# バケット名は config.py で動的に生成されます
# 形式: dev-on-aws-{STUDENT_ID}-{ACCOUNT_ID}
# 
# 注意: この値は config.py で一元管理されており、
# ここで上書きすることはできません。
# バケット名を変更したい場合は config.py を編集してください。

import sys
import os

# スクリプトのディレクトリを取得（どこから実行しても動作するように）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
from config import BUCKET_NAME

bucket_name = BUCKET_NAME

def get_local_path(filename):
    """スクリプトディレクトリ内のファイルパスを取得"""
    return os.path.join(SCRIPT_DIR, filename)
