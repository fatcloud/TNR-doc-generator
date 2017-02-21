from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from wsgiref.util import FileWrapper

import shutil
import zipfile
import subprocess




def home(request):

    if request.method == 'POST':

        dataset = request.FILES['dataset']
        # save dataset (overwrite the original one)
        with open('tnvrform/input.xlsx', 'wb') as destination:
            for chunk in dataset.chunks():
                destination.write(chunk)

        # save photoset
        photoset = request.FILES.get('photoset', None)
        shutil.rmtree('tnvrform/img/')
        if photoset is not None:
            zf = zipfile.ZipFile(photoset, mode='r')
            zf.extractall('tnvrform/img/')

        # execute for generator
        p = subprocess.Popen(['python', 'form_filler.py'], cwd='tnvrform')
        p.wait()

        filename = 'tnvrform/output.pdf'
        with open(filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        # response['Content-Length'] = getsize(filename)
        return response

    else:

        return render(
            request,
            'home.html',
            {}
    )



# generate the file
def proc_msg(request):

    response = render(
        request,
        'result.html',
        {},
    )
    # 一個顯示下載連結的頁面：若沒有自動開始下載請按此
    response = HttpResponse('<p>hahaha</p>')
    return response
