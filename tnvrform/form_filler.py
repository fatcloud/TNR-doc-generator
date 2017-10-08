#! /usr/bin/env python

from input_loader import TNVRDataLoader as loader
from form_exporter import generate_all_forms

from reportlab.lib.utils import ImageReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, black
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
        {'item':'Ta1', 'type':'str'   , 'source':'row[7]', 'coord':(180, 689)},
        {'item':'Ta2', 'type':'opt'   , 'source':'row[8]', 'coord':{'公':(184,663),'母':(329,663)}},
        {'item':'Ta3', 'type':'opt'   , 'source':'row[9]', 'coord':{'嬰':(220,637),'幼':(178,625),'成':(297,638),'老':(253,625)}},
        {'item':'Ta4', 'type':'opt'   , 'source':'value(row[1])', 'coord':{'無':(221,601),'有':(167,587)}},
        {'item':'Ta4r', 'type':'str'  , 'source': 'reason(row[1])', 'coord':(197,587)},
        {'item':'Timg', 'type':'img'  , 'source':'row[3]+\'e\'', 'coord':(429,575), 'width':130},
        {'item':'Tb1', 'type':'str'   , 'source':'\'陳淑娟\'', 'coord':(193,556)}, #constant?
        {'item':'Tb2', 'type':'str'   , 'source':'str(row[2])', 'coord':(225,533)},
        {'item':'Tb3a', 'type':'str'  , 'source':'row[4]', 'coord':(193,510)},
        {'item':'Tb3b', 'type':'str'  , 'source':'row[5]', 'coord':(220,510)},
        {'item':'Tb4', 'type':'str'  , 'source':'row[6]', 'coord':(225,495)},
        {'item':'Tb51', 'type':'str'  , 'source':'\'公告於懷生相信動物協會FB公開版面\'', 'coord':(232,482)}, #constant?
        {'item':'Tb52', 'type':'str'  , 'source':'period(row[2])', 'coord':(232,472)}, 
        {'item':'NV1', 'type':'str'  , 'source':'str(row[10])', 'coord':(224,455)},
        {'item':'NV2', 'type':'opt'  , 'source':'row[8]', 'coord':{'公':(205,435), '母':(265,435)}},
        {'item':'NV3', 'type':'opt'  , 'source':'value(row[14])', 'coord':{'否':(238, 417),'是':(172,396)}},
        {'item':'NV3r', 'type':'str' , 'source':'reason(row[14])', 'coord':(253,396)},
        {'item':'NV4', 'type':'opt'  , 'source':'value(row[15])', 'coord':{'否':(195, 378),'是':(256,376),'安樂死':(200,357)}},
        {'item':'NV4r1', 'type':'str', 'source':'reason(row[15]) if \'是\' in row[15][0] else \' \'', 'coord':(310,377)},
        {'item':'NV4r2', 'type':'str', 'source':'reason(row[15]) if \'安樂死\' in row[15] else \' \'', 'coord':(288,358)},
        {'item':'NV5', 'type':'opt'  , 'source':'row[8]', 'coord':{'公':(207, 339),'母':(267,339)}},
        {'item':'NV6', 'type':'str'  , 'source':'str(row[13])', 'coord':(238, 310)},
        {'item':'NV7', 'type':'opt'  , 'source':'\'有\'', 'coord':{'有':(238, 282),'無':(333,280)}}, #constant option
        {'item':'NVimg', 'type':'img' , 'source':'row[3]+\'o\'', 'coord':(429, 255), 'width':130},
        {'item':'R1', 'type':'str'   , 'source':'str(row[11])', 'coord':(219, 242)},
        {'item':'R2', 'type':'opt'   , 'source':'\'補助\'', 'coord':{'補助':(188, 203),'自費':(257, 203)}}, #constant option
        #'Rimg' : {'type':'img' , 'source':'stamp', 'coord':(197, 118)},
        {'item':'Rr', 'type':'str' , 'source':'row[41] if row[41] is not None else \'\'', 'coord':(424, 117)},
        {'item':'final', 'type':'str' , 'source':'\'V\'', 'coord':(52, 71)}
    ]
    canvas.setFont('STHeiti', 10)
    canvas.setFillColor(black)

    for item in form_items:
        itype, isource, icoord = item['type'], item['source'], item['coord']

        try:

            if itype == 'opt':
                xx, yy = icoord[eval(isource)]
                icoord[eval(isource)] = xx * 0.98, yy * 1.04
            else:
                xx, yy = icoord
                icoord = xx * 0.98, yy * 1.04

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
                xx, yy = coord
                if itype not in ['str', 'img']:
                    coord = xx * 0.98, yy * 1.04
                canvas.rect(*coord , 10.0, 10.0, fill=1, stroke=0)
            canvas.setFillColor(black)


if __name__ == '__main__':
    #xlsx_data = loader('data/error_example.xlsx').data
    xlsx_data = loader('input.xlsx').data
    generate_all_forms( data_set=xlsx_data,
                        form_filler=tnvr_form_filler,
                        out_filename='output.pdf',
                        template = 'data/template.pdf')
