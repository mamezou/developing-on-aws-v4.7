# S3 Resource API サンプル

boto3 の高レベル API (resource) を使用した S3 操作サンプルです。

## 学習目標

このデモを通じて以下を学びます：

1. **Resource API の基本** - `boto3.resource('s3')` の使い方
2. **オブジェクト指向アプローチ** - Bucket, Object クラスの操作
3. **Client API との違い** - コードの簡潔さ、戻り値の違い
4. **高度な操作** - マルチパート転送、署名付き URL 生成

## Resource API vs Client API

| 項目 | Resource API | Client API |
|------|--------------|------------|
| レベル | 高レベル（抽象化） | 低レベル（AWS API に近い） |
| 戻り値 | オブジェクト | dict（レスポンス全体） |
| コード量 | 少ない | やや多い |
| 直感性 | 高い | 中程度 |
| 用途 | シンプルな操作 | 細かい制御が必要な場合 |

### コード比較例

```python
# Resource API（シンプル）
s3 = boto3.resource('s3')
bucket = s3.Bucket('my-bucket')
bucket.upload_file('local.txt', 'remote.txt')

# Client API（詳細な制御）
s3 = boto3.client('s3')
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')
```

## 推奨実行順序

```
1. resource01-create-bucket.py    # バケット作成
      ↓
2. resource02-put-object.py       # オブジェクト格納（put）
   resource03-upload-file.py      # ファイルアップロード
      ↓
3. resource06-list-object.py      # オブジェクト一覧
      ↓
4. resource04-get-object.py       # オブジェクト取得（get）
   resource05-download-file.py    # ファイルダウンロード
      ↓
5. resource10-presigned_url.py    # 署名付き URL 生成
      ↓
6. resource07-delete-object.py    # オブジェクト削除
      ↓
7. resource11-delete-bucket.py    # バケット削除
```

## ファイル一覧

### 設定・データ
| ファイル | 説明 |
|----------|------|
| `mybucket.py` | バケット名設定（config.py と連携） |
| `AWSIcons.zip` | マルチパート転送用サンプル（大きいファイル） |
| `cat.jpg`, `Eiffel.jpg` | サンプル画像 |

### バケット操作
| ファイル | 説明 | 使用クラス/メソッド |
|----------|------|---------------------|
| `resource00-list-bucket.py` | バケット一覧取得 | `s3.buckets.all()` |
| `resource01-create-bucket.py` | バケット作成 | `s3.create_bucket()` |
| `resource-bucket-exist-check.py` | バケット存在チェック | `bucket.creation_date` |
| `resource11-delete-bucket.py` | バケット削除 | `bucket.delete()` |

### オブジェクト操作
| ファイル | 説明 | 使用クラス/メソッド |
|----------|------|---------------------|
| `resource02-put-object.py` | オブジェクト格納 | `obj.put()` |
| `resource03-upload-file.py` | ファイルアップロード | `bucket.upload_file()` |
| `resource04-get-object.py` | オブジェクト取得 | `obj.get()` |
| `resource05-download-file.py` | ファイルダウンロード | `bucket.download_file()` |
| `resource06-list-object.py` | オブジェクト一覧 | `bucket.objects.all()` |
| `resource07-delete-object.py` | オブジェクト削除 | `obj.delete()` |

### 高度な操作
| ファイル | 説明 | 使用クラス/メソッド |
|----------|------|---------------------|
| `resource08-multipart-upload.py` | マルチパートアップロード | `bucket.upload_file()` with `TransferConfig` |
| `resource09-multipart-download.py` | マルチパートダウンロード | `bucket.download_file()` with `TransferConfig` |
| `resource10-presigned_url.py` | 署名付き URL 生成 | `s3.meta.client.generate_presigned_url()` |

## 実行方法

```bash
# ディレクトリ移動
cd modules/module05/advanced/resource_api

# バケット作成
python3 resource01-create-bucket.py

# ファイルアップロード
python3 resource03-upload-file.py

# オブジェクト一覧
python3 resource06-list-object.py

# クリーンアップ
python3 resource11-delete-bucket.py
```

## バケット名について

`mybucket.py` は `config.py` と連携しており、環境変数 `STUDENT_ID` に基づいて動的にバケット名が生成されます。

形式: `dev-on-aws-{STUDENT_ID}-{ACCOUNT_ID}`

## 参考

- [boto3 S3 Resource API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#service-resource)
- [S3 Bucket Resource](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#bucket)
- [S3 Object Resource](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object)
