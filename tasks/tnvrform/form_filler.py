#! /usr/bin/env python

from input_loader import TNVRDataLoader as loader
from form_exporter import generate_all_forms

from reportlab.lib.utils import ImageReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab.lib.fonts


pdfmetrics.registerFont(TTFont('STHeiti','data/STHeiti-Medium.ttc'))

#reportlab.lib.fonts.ps2tt = lambda psfn: ('STHeiti', 0, 0)
#reportlab.lib.fonts.tt2ps = lambda fn,b,i: 'STHeiti'


def tnvr_form_filler(data_row, canvas):
    
    # 顯示每一筆輸入資料
    print('Here is a single row:', data_row, '\n')
    
    # 示範貼上文字
    # canvas.setFont()
    print(pdfmetrics.getRegisteredFontNames())
    canvas.setFont('STHeiti', 12)
    canvas.setFillColorRGB(1,0,0)
    canvas.drawString(10, 100, ' '.join(map(str, data_row)))

    # 示範貼上圖片
    im = ImageReader("img/cat.jpg")
    canvas.drawImage(im, 50, 10, width=100,height=100)

    # ========= 以上為示範程式碼，需刪除後才能開始正式工作
    # TODO    



if __name__ == '__main__':
    xlsx_data = loader('data/example.xlsx').data
    generate_all_forms( data_set=xlsx_data,
                        form_filler=tnvr_form_filler,
                        out_filename='output.pdf',
                        template = 'data/template.pdf')
