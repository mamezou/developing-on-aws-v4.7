# S3 Client API サンプル

boto3 の低レベル API (client) を使用した S3 操作サンプルです。

## 学習目標

このデモを通じて以下を学びます：

1. **Client API の基本** - `boto3.client('s3')` の使い方
2. **オブジェクト操作** - put_object, get_object, upload_file, download_file の違い
3. **高度な操作** - マルチパート転送、署名付き URL 生成
4. **エラーハンドリング** - boto3 の例外処理パターン

## Client API vs Resource API

| 項目 | Client API | Resource API |
|------|------------|--------------|
| レベル | 低レベル（AWS API に近い） | 高レベル（抽象化） |
| 戻り値 | dict（レスポンス全体） | オブジェクト |
| 柔軟性 | 高い | 中程度 |
| コード量 | やや多い | 少ない |
| 用途 | 細かい制御が必要な場合 | シンプルな操作 |

## 推奨実行順序

```
1. client01-create-bucket.py    # バケット作成
      ↓
2. client02-put-object.py       # オブジェクト格納（put_object）
   client03-upload-file.py      # ファイルアップロード（upload_file）
      ↓
3. client07-list-object.py      # オブジェクト一覧
      ↓
4. client04-get-object.py       # オブジェクト取得（get_object）
   client05-download-file.py    # ファイルダウンロード（download_file）
      ↓
5. client11-presigned_url.py    # 署名付き URL 生成
      ↓
6. client08-delete-object.py    # オブジェクト削除
      ↓
7. client12-delete-bucket.py    # バケット削除
```

## ファイル一覧

### 設定・データ
| ファイル | 説明 |
|----------|------|
| `mybucket.py` | バケット名設定（config.py と連携） |
| `AWSIcons.zip` | マルチパート転送用サンプル（大きいファイル） |
| `cat.jpg`, `Eiffel.jpg` | サンプル画像 |
| `item.csv` | サンプル CSV |

### バケット操作
| ファイル | 説明 | 使用 API |
|----------|------|----------|
| `client00-list-bucket.py` | バケット一覧取得 | `list_buckets()` |
| `client01-create-bucket.py` | バケット作成 | `create_bucket()` |
| `client-bucket-exist-check.py` | バケット存在チェック | `head_bucket()` |
| `client12-delete-bucket.py` | バケット削除 | `delete_bucket()` |

### オブジェクト操作
| ファイル | 説明 | 使用 API |
|----------|------|----------|
| `client02-put-object.py` | オブジェクト格納 | `put_object()` |
| `client03-upload-file.py` | ファイルアップロード | `upload_file()` |
| `client04-get-object.py` | オブジェクト取得 | `get_object()` |
| `client05-download-file.py` | ファイルダウンロード | `download_file()` |
| `client06-upload-download-fileobj.py` | メモリ上のデータ転送 | `upload_fileobj()`, `download_fileobj()` |
| `client07-list-object.py` | オブジェクト一覧 | `list_objects_v2()` |
| `client08-delete-object.py` | オブジェクト削除 | `delete_object()` |

### 高度な操作
| ファイル | 説明 | 使用 API |
|----------|------|----------|
| `client09-multipart-upload.py` | マルチパートアップロード | `upload_file()` with `TransferConfig` |
| `client10-multipart-download.py` | マルチパートダウンロード | `download_file()` with `TransferConfig` |
| `client11-presigned_url.py` | 署名付き URL 生成 | `generate_presigned_url()` |

## 実行方法

```bash
# ディレクトリ移動
cd modules/module05/advanced/client_api

# バケット作成
python3 client01-create-bucket.py

# ファイルアップロード
python3 client03-upload-file.py

# オブジェクト一覧
python3 client07-list-object.py

# クリーンアップ
python3 client12-delete-bucket.py
```

## バケット名について

`mybucket.py` は `config.py` と連携しており、環境変数 `STUDENT_ID` に基づいて動的にバケット名が生成されます。

形式: `dev-on-aws-{STUDENT_ID}-{ACCOUNT_ID}`

## 参考

- [boto3 S3 Client API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
- [S3 Transfer Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html#using-the-transfer-manager)
