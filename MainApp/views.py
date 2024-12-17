from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from .forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {'pagename': 'Добавление нового сниппета', 'form': form}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snp = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', 'snps': snp}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, value):
    try:
        snp = Snippet.objects.get(id=value)
    except ObjectDoesNotExist: return HttpResponse(f'<ul><h4>сниппета под номером {value} не существует</h4></ul>')
    else:
        val = {'snip': snp}
        return render(request, 'pages/snippet.html', val)
    

def create_snippet(request):
    from pprint import pprint
    if request.method == "POST":
        pprint(request.POST)
        return HttpResponse('DONE')

