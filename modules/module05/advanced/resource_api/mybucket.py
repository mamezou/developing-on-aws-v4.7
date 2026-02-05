# バケット名は config.py で動的に生成されます
# 形式: dev-on-aws-{STUDENT_ID}-{ACCOUNT_ID}
# 
# 注意: この値は config.py で一元管理されており、
# ここで上書きすることはできません。
# バケット名を変更したい場合は config.py を編集してください。

import sys
sys.path.insert(0, '../../../../')
from config import BUCKET_NAME

bucket_name = BUCKET_NAME
