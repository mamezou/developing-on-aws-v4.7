# 自習用サンプル（Optional）

このディレクトリは講義では使用しません。
興味のある方が自習で参照するためのサンプル集です。

## client_api/
低レベル API (`boto3.client('dynamodb')`) を使用した DynamoDB 操作

特徴:
- 型記述子が必要: `{'S': 'value'}`, `{'N': '123'}`
- AWS API に近い形式
- PartiQL が使える

## resource_api/
ドキュメントインターフェイス (`boto3.resource('dynamodb')`) を使用した DynamoDB 操作

特徴:
- 型記述子不要、Python型で直接操作
- より直感的なコード
- movies_example/: AWS公式ドキュメントベースの包括的サンプル
