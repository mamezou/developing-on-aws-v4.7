# DynamoDB GSI マルチ属性キー デモ

2024年11月 GA のマルチ属性キー機能を体験するデモです。

## 概要

従来は GSI で複数属性を使ったクエリを行う場合、**合成キー**（文字列連結）を作成する必要がありました。
マルチ属性キー機能では、**最大4つの属性を直接キーとして指定**でき、合成キーが不要になります。

## 従来の方法 vs マルチ属性キー

### ❌ 従来の方法（合成キー）

```python
# データ投入時に合成キーを手動で作成
item = {
    'order_id': 'ORD-001',
    'customer_id': 'CUST-123',
    'status': 'pending',
    'order_date': '2024-01-15',
    # 合成キーを手動で作成（面倒！）
    'gsi_pk': 'CUST-123',
    'gsi_sk': 'pending#2024-01-15#ORD-001'
}

# クエリ時も begins_with で前方一致
KeyConditionExpression='gsi_pk = :pk AND begins_with(gsi_sk, :prefix)'
```

### ✅ マルチ属性キー（新機能）

```python
# 自然な属性をそのまま保存（合成キー不要！）
item = {
    'order_id': 'ORD-001',
    'customer_id': 'CUST-123',
    'status': 'pending',
    'order_date': '2024-01-15'
}

# クエリも直感的
KeyConditionExpression='customer_id = :cid AND status = :status AND order_date >= :date'
```

## デモシナリオ

EC サイトの注文データで、以下を比較体験：

1. **従来方式のテーブル** - 合成キーを使った GSI
2. **マルチ属性キー方式のテーブル** - 新機能を使った GSI

同じクエリを両方で実行し、コードの簡潔さと結果を比較します。

## ファイル一覧

- `myconfig.py` - 設定ファイル
- `setup_table.py` - テーブル作成（両方式）
- `setup_data.py` - サンプルデータ投入
- `query_demo.py` - クエリ比較デモ
- `cleanup.py` - テーブル削除

## 実行手順

```bash
# ディレクトリ移動
cd modules/module07/advanced/dynamodb-gsi-multi-key

# 1. テーブル作成（従来方式 + マルチ属性キー方式）
python3 setup_table.py

# 2. サンプルデータ投入
python3 setup_data.py

# 3. クエリ比較デモ
python3 query_demo.py

# 4. クリーンアップ
python3 cleanup.py
```

## 学習ポイント

1. **コードの簡潔さ** - 合成キーの作成・パースが不要
2. **型安全性** - 各属性が独立しているため型を保持
3. **柔軟なクエリ** - 左から順に条件を指定可能
4. **既存テーブルへの適用** - 新しい GSI として追加可能

## 制約事項

- パーティションキー: 最大4属性
- ソートキー: 最大4属性
- ソートキーは**左から順に**条件を指定する必要がある

## 参考

- [Multi-attribute keys pattern - Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.DesignPattern.MultiAttributeKeys.html)
