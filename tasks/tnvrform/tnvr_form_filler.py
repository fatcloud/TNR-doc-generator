#! /usr/bin/env python

from tnvr_input_loader import TNVRDataLoader as loader
from tnvr_form_exporter import generate_all_forms

from reportlab.lib.utils import ImageReader


def tnvr_form_filler(data_row, canvas):
    
    # 顯示每一筆輸入資料
    print('Here is a single row:', data_row, '\n')
    
    # 示範貼上文字
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
