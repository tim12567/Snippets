from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from .models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required



def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def snippets_my(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {'pagename': 'Мои сниппеты', 'snps': snippets}
    return render(request, 'pages/view_snippets.html', context)


def create_user(request):
    context = {'pagename': 'Регистрация нового пользователя'}
    # создаем пустую форму при запросе GET
    if request.method == "GET":
        form = UserRegistrationForm()
        context['form'] = form
        return render(request, 'pages/registration.html', context)
    
    # Получаем данные из формы и на их основе создаем новый сниппет в БД 
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()       
            return redirect('home')
        context['form'] = form
        return render(request, 'pages/registration.html', context)


def snippets_page(request):
    snp = Snippet.objects.filter(public=True)
    context = {'pagename': 'Просмотр сниппетов', 'snps': snp}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, value):
    context = {'pagename': 'Просмотр сниппета'}
    try:
        snp = Snippet.objects.get(id=value)
    except ObjectDoesNotExist: return HttpResponse(f'<ul><h4>сниппета под номером {value} не существует</h4></ul>')
    else:
        comments_form = CommentForm()
        context['snip'] = snp
        context['type'] = 'view'
        context['comments_form'] = comments_form
        return render(request, 'pages/snippet.html', context)
    

@login_required
def snippet_delete(request, value):
    if request.method == 'POST' or request.method == 'GET':
        snip = get_object_or_404(Snippet.objects.filter(user=request.user), id = value)
        snip.delete()
    return redirect('sp_list')


@login_required
def snippet_edit(request, value):
    try:
        sn_add = Snippet.objects.filter(user=request.user).get(id=value)
    except ObjectDoesNotExist: return Http404
    
    # хотим получить страницу с данными сниппета
    if request.method == "GET":
        context = {'snippet': sn_add, 'type': 'edit'}
        return render(request, 'pages/snippet.html', context)
    
    # Получаем данные из формы и на их основе создаем новый сниппет в БД 
    if request.method == "POST":
        data_form = request.POST
        print(f'{data_form = }')
        sn_add.name = data_form['name'] 
        sn_add.code = data_form['code']
        # если ключ public есть в словаре то берем значение если нету то присваиваем False
        sn_add.public = data_form.get('public', False)
        sn_add.creation_date = data_form['creation_date']
        sn_add.save()
        return redirect('sp_list')
    

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'pagename': 'PythonBin',
                'errors': ['некорректно введен пароль либо имя пользователя'],
            }
            return render(request, 'pages/index.html', context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')
   

@login_required(login_url='home')
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
            # создает но не сохраняет
            snippet = form.save(commit=False)
            # если пользователь залогинен, тогда мы сохраняем сниппет с таким пользователем
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect('sp_list')
        return render(request, 'pages/add_snippet.html', {'form': form})
    

@login_required
def comments_add(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get('snippet_id')
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect('sp_val', snippet_id = snippet.id)
    return HttpResponseNotAllowed(['POST'])