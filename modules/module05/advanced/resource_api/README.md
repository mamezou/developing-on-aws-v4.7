# S3 Resource API サンプル

boto3 の高レベル API (resource) を使用した S3 操作サンプルです。

## 準備

```bash
# AWS 認証情報の設定
aws configure
# または
aws sso login --profile <YOUR-PROFILE>

# 認証確認
aws sts get-caller-identity
```

## バケット名について

`mybucket.py` は `config.py` と連携しており、環境変数 `STUDENT_ID` に基づいて動的にバケット名が生成されます。

## サンプルファイル一覧

### 設定・データ
- `mybucket.py` - バケット名設定（config.pyと連携）
- `AWSIcons.zip` - サンプルデータ
- `cat.jpg`, `Eiffel.jpg` - サンプル画像

### バケット操作
- `resource-bucket-exist-check.py` - バケットの存在チェック
- `resource00-list-bucket.py` - バケット一覧取得
- `resource01-create-bucket.py` - バケット作成
- `resource11-delete-bucket.py` - バケット削除（オブジェクト含む）

### オブジェクト操作
- `resource02-put-object.py` - オブジェクト格納
- `resource03-upload-file.py` - ファイルアップロード
- `resource04-get-object.py` - オブジェクト取得
- `resource05-download-file.py` - ファイルダウンロード
- `resource06-list-object.py` - オブジェクト一覧取得
- `resource07-delete-object.py` - オブジェクト削除

### 高度な操作
- `resource08-multipart-upload.py` - マルチパートアップロード
- `resource09-multipart-download.py` - マルチパートダウンロード
- `resource10-presigned_url.py` - 署名付きURL生成

## 実行例

```bash
# バケット作成
python resource01-create-bucket.py

# ファイルアップロード
python resource03-upload-file.py

# オブジェクト一覧
python resource06-list-object.py

# クリーンアップ
python resource11-delete-bucket.py
```

## 参考

- [boto3 S3 Resource API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#service-resource)
