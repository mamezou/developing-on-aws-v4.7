# Copyright 2020 Amazon Web Services, Inc. or its affiliates. All rights reserved.
'''
  サンプルデータのロード
  
  moviedata.json から映画データを DynamoDB にロードします。
  LOAD_LIMIT で読み込む件数を制限できます（デモ用途では200件程度で十分）。
  全件ロードする場合は LOAD_LIMIT = None に設定してください。
'''
import json
import boto3
import os
from decimal import *
from myconfig import TABLE_NAME, REGION

def get_local_path(filename):
    """スクリプトと同じディレクトリにあるファイルのパスを取得"""
    return os.path.join(os.path.dirname(__file__), filename)

LOAD_LIMIT = 200  # ロードする最大件数（None で全件ロード）

def load_movies(movies, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=REGION)

    table = dynamodb.Table(TABLE_NAME)
    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        print("Adding movie:", year, title)
        table.put_item(Item=movie)


if __name__ == '__main__':
    with open(get_local_path("moviedata.json")) as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    
    # LOAD_LIMIT が設定されている場合は件数を制限
    if LOAD_LIMIT:
        movie_list = movie_list[:LOAD_LIMIT]
        print(f"ロード件数を {LOAD_LIMIT} 件に制限します")
    
    load_movies(movie_list)
    print(f"✅ {len(movie_list)} 件のデータをロードしました")
