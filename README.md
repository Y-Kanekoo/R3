# Project R3
データベース起動(root=user名)
mysql -u root -p;
データベース作成
CREATE DATABASE giveandgift;
データベース閲覧
show databases;
データベース選択
USE "name";
データベース削除
DROP DATABASE giveandgift;
テーブル一覧(USEで選択していればFROM以降いらない)
SHOW TABLES FROM "databasename";
テーブル削除
DROP TABLE "tablename";
テーブル内カラム情報
SHOW COLUMNS FROM "tablename" FROM "databasename";
SHOW COLUMNS FROM "employee" FROM "giveandgift";
テーブル内削除
DELETE FROM "tablename";
テーブルの構造を見る
DESCRIBE thresholds;

仮想環境設定(myproject-master直下で起動)
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt

データベース変更方法
settings.pyでデータベースを変更
migrationsの中の_init_.以外を消す
myproject-master\myproject-masterで
python manage.py makemigrations
python manage.py migrate

データベースの全データ削除
python manage.py flush
python manage.py runscript insert_demo_data
python manage.py runserver

クローン
git clone "address"
リモートリポジトリ名の調べ方
git remote
データを持ってくる
git pull リモートリポジトリ名　ブランチ名(ksho)
git pull origin mastar



フォークしてプルリクエストを送る
1 リポジトリのフォーク
	フォークしたいアカウントのリポジトリ R3.git を自分のGitHubアカウントに
	フォークします。フォークボタンはリポジトリの右上にあります。
2 クローン
	git clone "address"
3 クローン下ディレクトリに移動
	cd R3
4 ブランチの作成(例:kshoという名前)
	git checkout -b ksho
5 変更を加える
6 コミットしてプッシュ
	git add .
	git commit -m "branch chenge ksho"
	git push origin ksho
7 プルリクエストの作成(githubで)hata


プロジェクト内に新しいアプリケーションを作る手順
1 pollsという名前のディレクトリを作成
	py manage.py startapp polls

2 ビューの作成
	polls/views.py
	from django.http import HttpResponse
		def index(request):
	    return HttpResponse("Hello, world. You're at the polls index.")

3 urls.pyの作成
	polls/urls.py
	from django.urls import path
	from . import views
	urlpatterns = [
	    path("", views.index, name="index"),
	]

4 グローバルurlへの追加
	myproject/urls.py
	from django.contrib import admin
	from django.urls import include, path

	urlpatterns = [
	    path("polls/", include("polls.urls")),
	    path("admin/", admin.site.urls),
	]

5 ページへアクセス
	py manage.py runserver
	http://localhost:8000/polls/ 

ディレクトリの階層
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py

Djangoの静的ファイルについて
静的ファイルは、主にCSS、JavaScript、画像などのクライアントサイドで使用されるリソースを
管理するためのものです
myproject/
│
├── myapp/
│   ├── static/ ##ここにディレクトリ作成　その中に css, js, imagesなどのサブフォルダを作成
│   │   ├── myapp/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   ├── templates/
│   └── ...
│
├── manage.py
└── settings.py

#settings.pyの設定
STATIC_URL = '/static/'
# 静的ファイルを格納するディレクトリ
STATICFILES_DIRS = [
    BASE_DIR / "myapp/static",
]
# collectstaticコマンドで集めるディレクトリ
STATIC_ROOT = BASE_DIR / "staticfiles"

#css適応例
 <link rel="stylesheet" href="{% static 'myapp/css/show_daily_report_style.css' %}">
 
 ローカル開発環境でサーバーを立てる前に、以下のコマンドを実行します。
 python manage.py collectstatic

これでローカル環境で作った静的なファイルが格納されている"static"から"staticfiles"に
格納される。"staticfiles"は静的ファイル管理用

プルリクエストから、失敗したところを右クリック

Revartを選択して、プルリクエストを作成
作成したプルリクエストをマージする
あら不思議、失敗する前に戻りました。
参考：[GitHubでマージしちゃった特定のプルリクを取り消したい！ #プログラミング勉強日記 - Qiita](https://qiita.com/toranoko92114/items/d2213cf56d9749400599)

- プロジェクト内に新しいアプリケーションを作成して
python [manage.py](http://manage.py) migrateをしたときに、
→django.db.utils.OperationalError: (1050, "Table 'daily_reports' already exists")
こんなエラーが出たときは、
python [manage.py](http://manage.py/) migrate --fake <app_name>  
# <app_name> は daily_reports が属するアプリの名前
これでいったん解決できる

# ブランチを作成してそれをリモートに上げる手順
ローカルのmasterに行く
git checkout master　
リモートの最新の master ブランチを取得
git pull origin master 
 新しいブランチを作成し、そのブランチに移動
git checkout -b 新しいブランチ名
リモートにもブランチを作成し、追跡設定をする
git push -u origin 新しいブランチ名 

ブランチの消すコマンド
git branch -d 正しいブランチ名
もしローカルブランチを強制削除する場合
git branch -D 正しいブランチ名