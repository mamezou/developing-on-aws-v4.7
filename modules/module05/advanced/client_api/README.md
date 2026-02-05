# S3 Client API サンプル

boto3 の低レベル API (client) を使用した S3 操作サンプルです。

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
- `item.csv` - サンプルCSV

### バケット操作
- `client-bucket-exist-check.py` - バケットの存在チェック
- `client00-list-bucket.py` - バケット一覧取得
- `client01-create-bucket.py` - バケット作成
- `client12-delete-bucket.py` - バケット削除（オブジェクト含む）

### オブジェクト操作
- `client02-put-object.py` - オブジェクト格納
- `client03-upload-file.py` - ファイルアップロード
- `client04-get-object.py` - オブジェクト取得
- `client05-download-file.py` - ファイルダウンロード
- `client06-upload-download-fileobj.py` - 変数データのアップロード/ダウンロード
- `client07-list-object.py` - オブジェクト一覧取得
- `client08-delete-object.py` - オブジェクト削除

### 高度な操作
- `client09-multipart-upload.py` - マルチパートアップロード
- `client10-multipart-download.py` - マルチパートダウンロード
- `client11-presigned_url.py` - 署名付きURL生成

## 実行例

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

## 参考

- [boto3 S3 Client API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
