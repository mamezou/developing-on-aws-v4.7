# NoSQL Workbench セットアップガイド

NoSQL Workbench は DynamoDB のデータモデリング、可視化、クエリ開発ができる GUI ツールです。
DynamoDB Local も内蔵しており、ローカル環境での開発・テストに便利です。

## ダウンロード・インストール

1. [NoSQL Workbench ダウンロードページ](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html) にアクセス

2. OS に合わせてダウンロード:
   - Windows: `.exe` インストーラー
   - macOS: `.dmg` ファイル
   - Linux: `.AppImage` ファイル

3. インストーラーを実行

## DynamoDB Local の起動

NoSQL Workbench には DynamoDB Local が内蔵されています。

1. NoSQL Workbench を起動
2. 左メニューから「Operation builder」を選択
3. 「Add connection」をクリック
4. 「DynamoDB local」タブを選択
5. 「Open DynamoDB local」をクリックして起動

デフォルトで `http://localhost:8000` で起動します。

## AWS CLI からの接続確認

DynamoDB Local が起動したら、CLI から接続できます:

```bash
# テーブル一覧を取得
aws dynamodb list-tables --endpoint-url http://localhost:8000

# テーブル作成テスト
aws dynamodb create-table \
    --table-name TestTable \
    --attribute-definitions AttributeName=pk,AttributeType=S \
    --key-schema AttributeName=pk,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:8000

# 確認
aws dynamodb list-tables --endpoint-url http://localhost:8000

# クリーンアップ
aws dynamodb delete-table --table-name TestTable --endpoint-url http://localhost:8000
```

## Python からの接続

```python
import boto3

# DynamoDB Local に接続
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000'
)

# テーブル一覧
for table in dynamodb.tables.all():
    print(table.name)
```

## 注意事項

- DynamoDB Local はメモリ上で動作するため、NoSQL Workbench を終了するとデータは消えます
- 本番環境の DynamoDB とは一部挙動が異なる場合があります
- WSL から localhost:8000 に接続できない場合は、Windows 側で NoSQL Workbench を起動し、WSL からは `host.docker.internal:8000` や Windows の IP アドレスを指定してください

## 参考リンク

- [NoSQL Workbench for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html)
- [DynamoDB Local の使用](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
