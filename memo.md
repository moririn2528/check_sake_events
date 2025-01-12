# firestore

ネイティブモードを選択、(default) のままにしないと無料枠から外れる
asia-northeast1 のシングルリージョンを選択

## log

API を投げてエラーが出たときは、監査ログからその API のログ権限を与える。
その後、Log explorer or IAM サービスキーのサービスアカウントログの使用ログから見ることが可能

firestore に対する権限が datastore.\* であることに注意。

## emulator

gcloud components update
gcloud emulators firestore start --host-port=localhost:8154
GUI に良いものがないため、保留

# deployment

gcloud auth application-default login することでデフォルト認証を設定できる
有効化はエラーメッセージからやる必要がある

# iam

サービス使用者はサービスアカウントを使っているとして、サービスに対して SetIAM を行う。
cloud functions が cloud firestore を使うときは firestore で setIAMPolicy をしないといけないが、firestore の client で setIAM はない。firestore やばい、firebase のせい？で統一できてない。iam ライブラリの API もやばめだったので、撤退。
(project-number)-compute@developer.gserviceaccount.com に対して _datastore_ ユーザー権限を gui から与えるのが楽。
firestore では検索できないので注意。

権限設定した後、function を作り直す必要がありそう？

# scrapy

cloud functions だと、signal 系によるエラーが出る。子プロセスに配置
https://weautomate.org/articles/running-scrapy-spider-cloud-function/

メモリ 256MB だと、200 個もクロールできないため、手動 gc.collect

# genkit

dotprompt docs: https://github.com/firebase/genkit/blob/main/docs/dotprompt.md

dotprompt を用いたとき、model: vertexai/gemini-1.5-flash にしていると

```
Model "vertexai/gemini-1.5-flash" not found
```

とエラーが出た。plugins に googleAI() を入れ、@genkit-ai/googleai/gemini15Flash のモデルにして解決。
