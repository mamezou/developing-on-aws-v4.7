# Strangler Fig Pattern（締め殺しパターン）

モノリシックアプリケーションをマイクロサービスに段階的に移行するためのデザインパターン。

## 概要

「締め殺しの木（Strangler Fig）」は、宿主の木に巻きついて徐々に置き換わる植物に由来する名前です。
同様に、レガシーシステムを稼働させたまま、機能を少しずつ新システムに移行していきます。

```
【移行前】
クライアント → モノリス（機能A, B, C, D）

【移行中】
クライアント → ファサード（API Gateway/ALB）
                    ├→ 新サービスA（Lambda/コンテナ）
                    ├→ 新サービスB（Lambda/コンテナ）
                    └→ モノリス（機能C, D）← 残りの機能

【移行後】
クライアント → ファサード
                    ├→ サービスA
                    ├→ サービスB
                    ├→ サービスC
                    └→ サービスD
```

## AWS での実装パターン

### 1. API Gateway をファサードとして使用
- パスベースルーティングで新旧を振り分け
- `/api/v2/*` → 新 Lambda
- `/api/v1/*` → 旧システム（HTTP 統合）

### 2. ALB をファサードとして使用
- パスベースまたはホストベースルーティング
- コンテナ（ECS/EKS）への移行に適している

### 3. Route 53 加重ルーティング
- DNS レベルでの段階的切り替え
- カナリアリリースとの組み合わせ

## メリット

- **リスク軽減**: 一度に全てを移行しない
- **段階的検証**: 機能ごとに動作確認できる
- **ロールバック容易**: 問題があれば旧システムに戻せる
- **ビジネス継続**: システム停止なしで移行

## 参考資料

### AWS 公式ドキュメント
- [Strangler Fig パターン - AWS 規範ガイダンス](https://docs.aws.amazon.com/ja_jp/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html)
- [Ten steps to modernizing legacy monoliths in the AWS Cloud](https://aws.amazon.com/jp/blogs/news/ten-steps-to-modernizing-legacy-monoliths-in-the-aws-cloud/)

### ワークショップ
- [Legacy to Modernization Workshop (re:Invent 2023)](https://catalog.us-east-1.prod.workshops.aws/workshops/f2c0706c-7192-495f-853c-fd3341db265a/en-US)
  - ECS、ALB、RDS を使った本格的なハンズオン
  - 所要時間: 2-3時間

### 解説記事
- [クラスメソッド: re:Invent 2023 ワークショップレポート](https://dev.classmethod.jp/articles/workshop-reinvent23-legacy-to-modernization/)
- [AWS Summit: コンテナモダナイゼーション資料 (PDF)](https://pages.awscloud.com/rs/112-TZM-766/images/AWS-48_Container_Modernization_KMD36.pdf)

## このコースとの関連

Module 11 の台本で触れている「モノリシックアプリケーションを疎結合化」の具体的な実装パターンです。

このコースで学ぶ技術との関連：
- **API Gateway** (Module 9): ファサードとして使用
- **Lambda** (Module 8): 新しいマイクロサービスの実装
- **Step Functions** (Module 11): 複雑なワークフローのオーケストレーション
- **SAM** (Module 13): マイクロサービスのデプロイ自動化
