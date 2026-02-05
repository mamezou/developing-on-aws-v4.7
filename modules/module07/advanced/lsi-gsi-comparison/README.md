# LSI vs GSI 比較デモ

ECサイトの注文テーブルを例に、LSI（ローカルセカンダリインデックス）と GSI（グローバルセカンダリインデックス）の違いを体験します。

## 根本的な違い

| 項目 | LSI | GSI |
|------|-----|-----|
| キー構成 | 同じPK、別のSK | 全く別のPK（とSK） |
| 作成タイミング | テーブル作成時のみ | いつでも追加・削除可能 |
| サイズ制限 | パーティションあたり10GB | なし |
| 整合性 | 強い整合性の読み込み可能 | 結果整合性のみ |

## シナリオ

### テーブル設計: Orders（注文）

```
PK: customer_id（顧客ID）
SK: order_date（注文日）
属性: order_id, product_id, status, amount
```

### LSI: 同じ顧客の注文を金額順で見たい

```
LSI: customer_id (PK) + amount (SK)
→「田中さんの注文を、高額順に表示」
```

### GSI: 商品ごとの売上を見たい

```
GSI: product_id (PK) + order_date (SK)
→「この商品が、いつ、どれだけ売れたか」
```

## 実行方法

```bash
# ディレクトリ移動
cd modules/module07/advanced/lsi-gsi-comparison

# 1. テーブル作成（LSI付き）→ GSI追加
python3 setup_table.py

# 2. サンプルデータ投入
python3 load_data.py

# 3. クエリ比較デモ
python3 query_demo.py

# 4. クリーンアップ
python3 cleanup.py
```

## 判断のポイント

| 状況 | 選択 |
|------|------|
| 同じPKで、ソートの切り口だけ増やしたい | LSI |
| 全く別の軸で検索したい | GSI |
| テーブル設計が固まっていない・後から変わりそう | GSI |
| パーティションあたり10GB超えそう | GSI |

実務では「後から追加できる」「柔軟性が高い」という理由で GSI を選ぶことが多いです。
