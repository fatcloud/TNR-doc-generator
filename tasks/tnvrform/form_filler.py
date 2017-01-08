#! /usr/bin/env python

from input_loader import TNVRDataLoader as loader
from form_exporter import generate_all_forms

from reportlab.lib.utils import ImageReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab.lib.fonts

from datetime import datetime,timedelta

pdfmetrics.registerFont(TTFont('STHeiti','data/STHeiti-Medium.ttc'))

#reportlab.lib.fonts.ps2tt = lambda psfn: ('STHeiti', 0, 0)
#reportlab.lib.fonts.tt2ps = lambda fn,b,i: 'STHeiti'


def tnvr_form_filler(row, canvas):
    
    '''
    # 顯示每一筆輸入資料
    print('Here is a single row:', row, '\n')
    
    # 示範貼上文字
    # canvas.setFont()
    print(pdfmetrics.getRegisteredFontNames())
    canvas.setFont('STHeiti', 12)
    canvas.setFillColorRGB(1,0,0)
    canvas.drawString(10, 100, ' '.join(map(str, row)))

    # 示範貼上圖片
    im = ImageReader("img/cat.jpg")
    canvas.drawImage(im, 50, 10, width=100,height=100)

    # ========= 以上為示範程式碼，需刪除後才能開始正式工作
    # TODO    
    '''

    def period(t):
        time = str(row[2])
        date = datetime.strptime(time, "%Y/%m/%d")
        db = date - timedelta(days = 8)
        de = date - timedelta(days = 1)
        period = db.strftime("%Y/%m/%d")+' - '+ de.strftime("%m/%d")
        return period
    


    form = {
        'Ta1' : {'type':'str' , 'source':'row[6]', 'coord':(190, 685)},
        'Ta2' : {'type':'opt' , 'source':'row[7]', 'coord':{'公':(193,662),'母':(347,662)}},
        'Ta3' : {'type':'opt' , 'source':'row[8]', 'coord':{'嬰':(227,637),'幼':(217,624),'成':(309,637),'老':(301,624)}},
        'Ta4' : {'type':'opt', 'source':'row[1].split(\'/\')[0]', 'coord':{'無':(233,600),'有':(233,587)}},
        'Ta4r' : {'type':'str', 'source':'\' \' if \'無\' in row[1] else row[1].split(\'/\')[-1]', 'coord':(257,587)},
        'Timg' : {'type':'img', 'source':'before', 'coord':(421,576)},
        'Tb1' : {'type':'str' , 'source':'\'某某某\'', 'coord':(203,550)}, #constant?
        'Tb2' : {'type':'str' , 'source':'str(row[2])', 'coord':(235,533)},
        'Tb3a' : {'type':'str' , 'source':'row[4]', 'coord':(213,510)},
        'Tb3b' : {'type':'str' , 'source':'row[5]', 'coord':(250,510)},
        'Tb41' : {'type':'str' , 'source':'\'公告於懷生相信動物協會FB公開版面\'', 'coord':(246,490)}, #constant?
        'Tb42' : {'type':'str' , 'source':'period(row[2])', 'coord':(246,473)}, 
        'NVa1' : {'type':'str' , 'source':'str(row[9])', 'coord':(235,451)},
        'NVa2' : {'type':'opt' , 'source':'row[7]', 'coord':{'公':(216,434), '母':(280,434)}},
        'NVa3' : {'type':'opt' , 'source':'row[13].split(\'/\')[0]', 'coord':{'否':(251, 415),'是':(222,395)}},
        'NVa3r' : {'type':'str' , 'source':'\' \' if \'否\' in row[13] else row[13].split(\'/\')[-1]', 'coord':(305,395)},
        'NVa4' : {'type':'opt' , 'source':'row[14].split(\'/\')[0]', 'coord':{'否':(205, 376),'是':(256,376),'安樂死':(205,357)}},
        'NVa4r1' : {'type':'str' , 'source':'row[14].split(\'/\')[-1] if \'是\' in row[14][0] else \' \'', 'coord':(307,376)},
        'NVa4r2' : {'type':'str' , 'source':'row[14].split(\'/\')[-1] if \'安樂死\' in row[14] else \' \'', 'coord':(285,357)},
        'NVa5' : {'type':'opt' , 'source':'row[7]', 'coord':{'公':(216, 338),'母':(280,338)}},
        'NVa6' : {'type':'str' , 'source':'str(row[12])', 'coord':(238, 307)},
        'NVa7' : {'type':'opt' , 'source':'\'有\'', 'coord':{'有':(251, 280),'無':(333,280)}}, #constant option
        'NVimg' : {'type':'img' , 'source':'after', 'coord':(421, 307)},
        'Ra1' : {'type':'str' , 'source':'str(row[10])', 'coord':(230, 240)},
        'Ra2' : {'type':'opt' , 'source':'\'補助\'', 'coord':{'補助':(200, 197),'自費':(257, 197)}}, #constant option
        #'Rimg' : {'type':'img' , 'source':'stamp', 'coord':(197, 118)},
        #'Rar': {'type':'str' , 'source':'row[40]', 'coord':(424, 117)},
    }
    canvas.setFont('STHeiti', 12)
    canvas.setFillColorRGB(1,0,0)

    for item in form.values():
        itype, isource, icoord = item['type'], item['source'], item['coord']
        if itype == 'str':
            canvas.drawString(*icoord, eval(isource))
        if itype == 'opt':
            canvas.drawString(*icoord[eval(isource)],'V')
        if itype == 'img':
            im = ImageReader("img/"+isource+".jpg")
            canvas.drawImage(im, *icoord, width=100,height=100)










if __name__ == '__main__':
    xlsx_data = loader('data/example.xlsx').data
    generate_all_forms( data_set=xlsx_data,
                        form_filler=tnvr_form_filler,
                        out_filename='output.pdf',
                        template = 'data/template.pdf')
