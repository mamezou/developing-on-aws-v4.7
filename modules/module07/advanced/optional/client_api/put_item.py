'''
  put_item を使用したデータのロード
  score_data.json のデータをテーブルに格納する
'''
import boto3
import botocore
import json
import os
from  myconfig import table_name

def get_local_path(filename):
    """スクリプトと同じディレクトリにあるファイルのパスを取得"""
    return os.path.join(os.path.dirname(__file__), filename)

# テーブルにデータをロードする関数
def load_data():
    # ファイルオープンとロード 
    f = open(get_local_path('score_data.json'))
    scores = json.load(f)  
    
    ddbClient = boto3.client('dynamodb')
    # ファイルのデータを put_item でテーブルに格納
    for rec in scores:
        item = {
            "userId": {"N": str(rec["userId"])},
            "gameId": {"S": rec["gameId"]},
            "score":  {"N": str(rec["score"])},
            "life":   {"N": str(rec["life"])}
        }
        ddbClient.put_item(TableName=table_name, Item=item)
        
    # ファイルのクローズ
    f.close()
    print("\nJSONファイルからのデータのロードが完了しました。\n")

# ここから実行開始
if __name__ == '__main__':
    try:
        load_data()
    except botocore.exceptions.ClientError as err:
        print(err.response['Error']['Message'])
    except botocore.exceptions.ParamValidationError as error:
        print(error)  
