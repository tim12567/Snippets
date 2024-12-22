from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from .models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    # создаем пустую форму при запросе GET
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', 'form': form}
        return render(request, 'pages/add_snippet.html', context)
    
    # Получаем данные из формы и на их основе создаем новый сниппет в БД 
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sp_list')
        return render(request, 'pages/add_snippet.html', {'form': form})


def snippets_page(request):
    snp = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', 'snps': snp}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, value):
    try:
        snp = Snippet.objects.get(id=value)
    except ObjectDoesNotExist: return HttpResponse(f'<ul><h4>сниппета под номером {value} не существует</h4></ul>')
    else:
        val = {'snip': snp, 'type': 'view'}
        return render(request, 'pages/snippet.html', val)
    

def snippet_delete(request, value):
    if request.method == 'POST' or request.method == 'GET':
        snip = get_object_or_404(Snippet, id = value)
        snip.delete()
    return redirect('sp_list')


def snippet_edit(request, value):
    try:
        sn_add = Snippet.objects.get(id=value)
    except ObjectDoesNotExist: return Http404

    # хотим получить страницу с данными сниппета
    if request.method == "GET":
        context = {'snippet': sn_add, 'type': 'edit'}
        return render(request, 'pages/snippet.html')
    
    # Получаем данные из формы и на их основе создаем новый сниппет в БД 
    if request.method == "POST":
        data_form = request.POST
        sn_add.name = data_form['name'] 
        sn_add.code = data_form['code']
        sn_add.creation_date = data_form['creation_date']
        sn_add.save()
        return redirect('sp_list')

    