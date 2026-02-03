# DynamoDB GSI マルチ属性キー デモ

2025年11月リリースの新機能。合成キー不要で複合条件クエリが可能になります。

## 概要

従来は GSI のソートキーに複数属性を使いたい場合、**合成キー**を作成する必要がありました。
新機能では、**最大4つの属性を直接ソートキーとして指定**できます。

## 従来の方法 vs 新機能

### ❌ 従来の方法（合成キー）

```python
# 合成キーを手動で作成
composite_key = f"{status}#{order_date}#{amount:010d}"

# クエリ時も手動でプレフィックス作成
KeyConditionExpression='customer_id = :cid AND begins_with(composite_key, :prefix)'
```

### ✅ 新機能（マルチ属性キー）

```python
# 合成キー不要！個別属性をそのまま保存
# クエリも直感的
KeyConditionExpression='customer_id = :cid AND status = :status AND order_date BETWEEN :start AND :end'
```

## デモシナリオ

EC サイトの注文データで、顧客ごとに以下のクエリを実行：
1. ステータスが "pending" の注文
2. ステータスが "pending" で、注文日が特定期間の注文
3. ステータスが "pending" で、注文日が特定期間で、金額が一定以上の注文

## ファイル一覧

- `template.yaml` - CloudFormation テンプレート
- `setup_data.py` - サンプルデータ投入スクリプト
- `query_demo.py` - クエリデモスクリプト

## 実行手順

```bash
# 1. テーブル作成（STUDENT_ID は環境変数から自動取得、または明示的に指定）
aws cloudformation create-stack \
  --stack-name demo-gsi-multi-key-${STUDENT_ID:-instructor} \
  --template-body file://template.yaml \
  --parameters ParameterKey=StudentId,ParameterValue=${STUDENT_ID:-instructor}

# 2. サンプルデータ投入
python3 setup_data.py

# 3. クエリデモ実行
python3 query_demo.py

# 4. クリーンアップ
aws cloudformation delete-stack --stack-name demo-gsi-multi-key-${STUDENT_ID:-instructor}
```

## 制約事項

- ソートキーは**左から順に**条件を指定する必要がある
- 最大4属性まで
- 既存の GSI の動作には影響なし

## ポイント

- 合成キー不要でクエリが直感的に
- 追加コストなし
- 既存テーブルにも適用可能（GSI 追加）
