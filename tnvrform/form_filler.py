#! /usr/bin/env python

from input_loader import TNVRDataLoader as loader
from form_exporter import generate_all_forms

from reportlab.lib.utils import ImageReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, red
import reportlab.lib.fonts

from datetime import datetime,timedelta

pdfmetrics.registerFont(TTFont('STHeiti','data/STHeiti-Medium.ttc'))

from glob import glob
import re


def tnvr_form_filler(row, canvas, row_index):

    def period(t):
        # convert 105/12/26 to 0105/12/26 to match YYYY/MM/DD pattern
        time = '0' + str(row[2])
        date = datetime.strptime(time, "%Y/%m/%d")
        db = date - timedelta(days = 8)
        de = date - timedelta(days = 1)
        period = db.strftime("%Y/%m/%d")+' - '+ de.strftime("%Y/%m/%d")
        return period
    
    
    def value(data):
        return data.split('/')[0]
    
    def reason(data):
        return data.split('/')[-1] if '/' in data else ''
         

    form_name = '台北市街犬絕育防疫 TNVR 執行計畫流程紀錄表'
    form_items = [
        {'item':'Ta1', 'type':'str'   , 'source':'row[6]', 'coord':(190, 685)},
        {'item':'Ta2', 'type':'opt'   , 'source':'row[7]', 'coord':{'公':(193,662),'母':(347,662)}},
        {'item':'Ta3', 'type':'opt'   , 'source':'row[8]', 'coord':{'嬰':(227,637),'幼':(217,624),'成':(309,637),'老':(301,624)}},
        {'item':'Ta4', 'type':'opt'   , 'source':'value(row[1])', 'coord':{'無':(233,600),'有':(233,587)}},
        {'item':'Ta4r', 'type':'str'  , 'source': 'reason(row[1])', 'coord':(257,587)},
        {'item':'Timg', 'type':'img'  , 'source':'row[3]+\'pre\'', 'coord':(421,576), 'width':120},
        {'item':'Tb1', 'type':'str'   , 'source':'\'陳淑娟\'', 'coord':(203,553)}, #constant?
        {'item':'Tb2', 'type':'str'   , 'source':'str(row[2])', 'coord':(235,533)},
        {'item':'Tb3a', 'type':'str'  , 'source':'row[4]', 'coord':(213,510)},
        {'item':'Tb3b', 'type':'str'  , 'source':'row[5]', 'coord':(250,510)},
        {'item':'Tb41', 'type':'str'  , 'source':'\'公告於懷生相信動物協會FB公開版面\'', 'coord':(246,490)}, #constant?
        {'item':'Tb42', 'type':'str'  , 'source':'period(row[2])', 'coord':(246,473)}, 
        {'item':'NVa1', 'type':'str'  , 'source':'str(row[9])', 'coord':(235,451)},
        {'item':'NVa2', 'type':'opt'  , 'source':'row[7]', 'coord':{'公':(216,434), '母':(280,434)}},
        {'item':'NVa3', 'type':'opt'  , 'source':'value(row[13])', 'coord':{'否':(251, 415),'是':(222,396)}},
        {'item':'NVa3r', 'type':'str' , 'source':'reason(row[13])', 'coord':(306,396)},
        {'item':'NVa4', 'type':'opt'  , 'source':'value(row[14])', 'coord':{'否':(205, 376),'是':(256,376),'安樂死':(205,357)}},
        {'item':'NVa4r1', 'type':'str', 'source':'reason(row[14]) if \'是\' in row[14][0] else \' \'', 'coord':(307,376)},
        {'item':'NVa4r2', 'type':'str', 'source':'reason(row[14]) if \'安樂死\' in row[14] else \' \'', 'coord':(285,357)},
        {'item':'NVa5', 'type':'opt'  , 'source':'row[7]', 'coord':{'公':(216, 338),'母':(280,338)}},
        {'item':'NVa6', 'type':'str'  , 'source':'str(row[12])', 'coord':(238, 307)},
        {'item':'NVa7', 'type':'opt'  , 'source':'\'有\'', 'coord':{'有':(251, 280),'無':(333,280)}}, #constant option
        {'item':'NVimg', 'type':'img' , 'source':'row[3]+\'post\'', 'coord':(421, 307), 'width':120},
        {'item':'Ra1', 'type':'str'   , 'source':'str(row[10])', 'coord':(230, 240)},
        {'item':'Ra2', 'type':'opt'   , 'source':'\'補助\'', 'coord':{'補助':(200, 197),'自費':(257, 197)}}, #constant option
        #'Rimg' : {'type':'img' , 'source':'stamp', 'coord':(197, 118)},
        {'item':'Rar', 'type':'str' , 'source':'row[40] if row[40] is not None else \'\'', 'coord':(424, 117)},
    ]
    canvas.setFont('STHeiti', 12)
    canvas.setFillColor(red)

    for item in form_items:
        itype, isource, icoord = item['type'], item['source'], item['coord']
        try:
            if itype == 'str':
                canvas.drawString(*icoord, eval(isource))
            if itype == 'opt':
                canvas.drawString(*icoord[eval(isource)],'V')
            if itype == 'img':
                img_exp = 'img/'+eval(isource)+'.*'
                img_name = glob(img_exp)[0]
                im = ImageReader(img_name)
                imw, imh = im.getSize()
                aspect = imh / float(imw)
                
                # determine the width and height
                w, h = item.get('width', None), item.get('height', None)
                if [w, h] == [None, None]:
                    w, h = 100, 100
                elif w is None:
                    w = h * aspect
                elif h is None:
                    h = w * aspect
                
                canvas.drawImage(im, *icoord, width=w,height=h)
        except:
            print('[Error] 自動填寫 ' + form_name + ' 的 ' + item['item'] + ' 項目時發生錯誤')
            
            column_indexs = []
            index_starts = [m.start()+4 for m in re.finditer('row\[', isource)]
            for idx in index_starts:
                idx_end = isource.find(']', idx)
                column_indexs.append(int(isource[idx : idx_end]))
            
            print('問題出在 xlsx 資料表中第 ' + str(row_index + 1) + ' 筆有效資料的第 ' + str(column_indexs) + ' 欄' )
            print('相關的欄位內容：')
            for index in column_indexs:
                print(row[index])
                
            canvas.setFillColor(Color(100, 100, 0, 0.5))
            coords = list(icoord.values()) if type(icoord) is dict else [icoord]

            for coord in coords:
                canvas.rect(*coord , 10.0, 10.0, fill=1, stroke=0)
            canvas.setFillColor(red)


if __name__ == '__main__':
    #xlsx_data = loader('data/error_example.xlsx').data
    xlsx_data = loader('input.xlsx').data
    generate_all_forms( data_set=xlsx_data,
                        form_filler=tnvr_form_filler,
                        out_filename='output.pdf',
                        template = 'data/template.pdf')
