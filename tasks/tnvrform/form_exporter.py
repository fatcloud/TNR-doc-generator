#! /usr/bin/env python

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter

from reportlab.lib.utils import ImageReader

from PyPDF2 import PdfFileMerger


def dummy_form_filler(row, canvas):
    
    # TODO
    # 示範貼上文字
    canvas.setFillColorRGB(1,0,0)
    canvas.drawString(10, 100, "Hello world")

    # 示範貼上圖片
    im = ImageReader("img/cat.jpg")
    canvas.drawImage(im, row * 50, 10, width=100,height=100)



def generate_form(data_row, form_filler, template, row_index):

    packet = io.BytesIO()

    # create a new PDF with Reportlab
    can = Canvas(packet, pagesize=letter)
    form_filler(data_row, can, row_index)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # read your existing PDF
    existing_pdf = PdfFileReader(open(template, "rb"))
    output = PdfFileWriter()

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    os = io.BytesIO()
    output.write(os)
    return os



def generate_all_forms(data_set, form_filler, out_filename, template):

    merger = PdfFileMerger()
    for row_index, row in enumerate(data_set):
        merger.append(generate_form(row, form_filler, template, row_index))

    with open(out_filename, 'wb') as fout:
        merger.write(fout)



if __name__ == '__main__':
    generate_all_forms( data_set = [2,1,5,9],
                        form_filler=dummy_form_filler,
                        out_filename='result.pdf',
                        template="data/template.pdf")
