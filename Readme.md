# 安裝 virtualenv
pip install virtualenv


# 為了方便處理中文字，以 python3 為基礎，創造一個名為 env 的環境（在現在的 project 資料夾下）
virtualenv -p python3 env


# 切換至 env 這個環境下
source env/bin/activate

若是 windows 系統則是

env\Scripts\activate.bat


# 為這個環境安裝 requirement.txt 裡提到的模組
pip install -r requirement.txt


# 要離開環境時呼叫
deactivate
