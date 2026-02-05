# Module 07 - DynamoDB 応用サンプル

## Python SDK の DynamoDB インターフェイス

スライドでは3種類のインターフェイスが紹介されていますが、Python (boto3) での対応は以下の通りです:

| スライドの分類 | Python (boto3) | 説明 |
|---------------|----------------|------|
| オブジェクト永続性 | ❌ なし | .NET, Java には DynamoDBMapper 等がある |
| ドキュメントインターフェイス | `boto3.resource('dynamodb')` | 型記述子不要、Python型で直接操作 |
| 低レベルインターフェイス | `boto3.client('dynamodb')` | 型記述子必要 `{'S': 'value'}` |

Python では「ドキュメントインターフェイス」相当の Resource API が実質的な高レベル API です。
オブジェクト永続性（ORM）が必要な場合は、サードパーティの [PynamoDB](https://pynamodb.readthedocs.io/) などを検討してください。

## デモ

### lsi-gsi-comparison/
LSI と GSI の違いを EC サイトの注文テーブルで体験するデモ

```bash
cd modules/module07/advanced/lsi-gsi-comparison

python3 setup_table.py   # テーブル作成（LSI付き）→ GSI追加
python3 load_data.py     # サンプルデータ投入
python3 query_demo.py    # クエリ比較
python3 cleanup.py       # クリーンアップ
```

### dynamodb-gsi-multi-key/
GSI マルチ属性キーのデモ（2025年11月新機能対応予定）

## 自習用（optional/）

講義ではデモしませんが、興味のある方は参照してください。

### optional/client_api/
低レベル API (`boto3.client('dynamodb')`) のサンプル集
- 型記述子 `{'S': 'value'}` を使った操作
- PartiQL、GSI追加など

### optional/resource_api/
ドキュメントインターフェイス (`boto3.resource('dynamodb')`) のサンプル集
- Python型での直接操作
- movies_example/: AWS公式ドキュメントベースのサンプル

## 参考

- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/)
- [boto3 DynamoDB Resource](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)
