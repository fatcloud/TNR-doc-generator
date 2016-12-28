# 自動填寫

這個任務是要寫一支小程式
依照 [填表範例](data/example.jpg) 的指示
把[這張表](data/input.xlsx)上的資料
自動填入 [台北市街犬防疫 TNVR 執行計畫流程紀錄表](data/template.pdf) 中。

輸入的資料表中會包涵很多列，每一列都要輸出一張表，
最後結果要存成一個包涵很多張表格的 pdf 檔案。

xlsx 檔案的輸出輸入將與其它的填表程式共用，故在這個任務中無須撰寫。


# 程式界面

參見 tnvr_form_filler.py，只要撰寫 TODO 部份完成單筆資料的填寫即可



# 參考資料

reportlab 的 pdf api [說明文件](https://www.reportlab.com/docs/reportlab-userguide.pdf)
