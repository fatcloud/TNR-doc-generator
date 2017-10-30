# 環境建置
----

先去裝好 python 3.5，接下來就用 python 內建的 pip 去安裝剩下的程式庫


安裝 virtualenv
```
$ pip install virtualenv
```
為了方便處理中文字，以 python3 為基礎，創造一個名為 env 的環境（在現在的 project 資料夾下）

```
$ virtualenv -p python3 env
```

切換至 env 這個環境下

```
$ source env/bin/activate
```

若是 windows 系統則是
```
$ env\Scripts\activate.bat
```

為這個環境安裝 requirement.txt 裡提到的模組
```
$ pip install -r requirements.txt
```

要離開環境時呼叫
```
$ deactivate
```

# 測試

先仿照環境建制提到的方式進入安裝好的 virtualenv 環境
接著去[這裡](https://www.miniwebtool.com/django-secret-key-generator/)產生一串 secret key
在命令列設定環境變數：

```
export DJANGO_DEBUG=True
export DJANGO_SECRET_KEY='<你剛剛產生的 secret key>'
```

把 <你剛剛產生的 secret key> 取代掉，注意留著那個單引號 ''，沒有單引號的話 secret key 裡面的字元很容易被誤為命令
最後執行

```
python3 manage.py runserver
```

這時候開瀏覽器連到本機的 locolhost:8000 就可以看到產生器了

pdf 產生器的程式碼在 ```TNR_forms_generator/tnvrform``` 這個資料夾下，欲了解與網站結構相關的事則見 [Django](https://docs.djangoproject.com/en/1.11/) 文件
