# Gourmet（Django料理投稿アプリ）

料理の投稿・閲覧ができる Django アプリです。  
`accounts` アプリでユーザー登録/ログイン、`dish` アプリで料理投稿・一覧・詳細表示・マイページ機能を提供します。

## 技術スタック

- Python 3.13
- Django 5.2
- PostgreSQL
- Gunicorn
- Nginx
- Docker / Docker Compose

## 主な機能

- ユーザー登録 / ログイン / ログアウト
- 料理投稿（画像アップロード対応）
- カテゴリ別一覧
- ユーザー別一覧
- 投稿詳細表示
- マイページ表示
- 投稿削除

## ディレクトリ構成（抜粋）

```text
.
├─ accounts/            # 認証・ユーザー関連
├─ dish/                # 料理投稿関連
├─ gourmet/             # Django設定・URL
├─ templates/           # 共通テンプレート
├─ static/              # 静的ファイル
├─ mediafiles/          # アップロード画像
├─ nginx/               # Nginx設定
├─ docker-compose.yaml
├─ Dockerfile
└─ requirements.txt
```

## セットアップ（Docker 推奨）

### 1. 環境変数ファイル作成

`.env_demo` をコピーして `.env` を作成してください。

```bash
cp .env_demo .env
```

Windows（cmd）の場合:

```cmd
copy .env_demo .env
```

必要に応じて `.env` の値（`SECRET_KEY`、DB接続情報など）を編集します。

### 2. コンテナ起動

```bash
docker compose up --build
```

起動後、アプリは以下でアクセスできます。

- アプリ: <http://localhost/>
- 管理画面: <http://localhost/admin/>

## DBマイグレーション

別ターミナルで以下を実行します。

```bash
docker compose exec web python manage.py migrate
```

## 管理ユーザー作成

```bash
docker compose exec web python manage.py createsuperuser
```

## 開発時によく使うコマンド

```bash
# ログ確認
docker compose logs -f

# 停止
docker compose down

# ボリュームごと削除して初期化
docker compose down -v
```

## ローカル実行（Dockerを使わない場合）

PostgreSQL を用意し、`.env` の接続情報を合わせた上で実行します。

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 補足

- 画像アップロードは `MEDIA_ROOT=mediafiles/` に保存されます。
- 静的ファイルは `STATIC_ROOT=staticfiles/` を利用します（本番は Nginx 経由配信）。
