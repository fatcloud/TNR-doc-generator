from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import zipfile
from wsgiref.util import FileWrapper

def home(request):
    # Handle file upload
    '''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    '''
    # Render list page with the documents and the form
    return render(
        request,
        'home.html',
        {}
    )



# generate the file
def result(request):
    post = request.POST
    #if post['taipei1'] == 'on':
        # 產生第一個表格檔案
    #    pass
    '''
    zfilename = 'forms.zip'
    zf = zipfile.ZipFile(zfilename, mode='w')
    try:
        print 'adding README.txt'
        zf.write('README.txt')
    finally:
        print 'closing'
        zf.close()    
    '''
    
    response = render(
        request,
        'home.html',
        {},
        content_type='application/zip'
    )
    # 一個顯示下載連結的頁面：若沒有自動開始下載請按此
    #response = HttpResponse(FileWrapper(myfile.getvalue()), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + zfilename
    return response

