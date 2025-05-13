"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from.forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import models
from .models import Blog
from .models import Comment # использование модели комментариев
from .forms import CommentForm,BlogForm # использование формы ввода комментар
from .models import Video
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница контактов.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Страница с описанием приложения.',
            'year':datetime.now().year,
        }
    )
def links(request):
    return render(request, 'app/links.html', {'title': 'Полезные ресурсы'})
def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {
        '1': 'Каждый день',
        '2': 'Несколько раз в день',
        '3': 'Несколько раз в неделю',
        '4': 'Несколько раз в месяц'
    }
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['internet'] = internet[form.cleaned_data['internet']]
            if form.cleaned_data['notice']:
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form': form,
            'data': data
        }
    )
def registration(request):
    """
    Renders the registration page.
    """
    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False  # запрещен вход в административный раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации

            reg_f.save()  # сохраняем изменения после добавления полей

            return redirect('home')  # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )
def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()  # Запрос на выбор всех статей блога из модели
    assert isinstance(request, HttpRequest)  # Проверка, что request является объектом HttpRequest
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',  # Передача заголовка страницы
            'posts': posts,   # Передача списка статей в шаблон
            'year': datetime.now().year,  # Передача текущего года
        }
    )
def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)  # Проверка, что request является объектом HttpRequest
    post_1 = Blog.objects.get(id=parametr)  # Запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=post_1)  # Получаем все комментарии для данной статьи

    if request.method == "POST":  # Обработка отправки формы
        form = CommentForm(request.POST)  # Создаем форму с данными из POST-запроса
        if form.is_valid():  # Проверяем валидность формы
            comment_f = form.save(commit=False)
            comment_f.author = request.user  # Добавляем авторизованного пользователя
            comment_f.date = datetime.now()  # Добавляем текущую дату
            comment_f.post = post_1  # Добавляем статью, к которой относится комментарий
            comment_f.save()  # Сохраняем комментарий
            return redirect('blogpost', parametr=post_1.id)  # Переадресация на ту же страницу
    else:
        form = CommentForm()  # Создаем пустую форму для GET-запроса

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,  # Передача конкретной статьи в шаблон
            'comments': comments,  # Передача списка комментариев в шаблон
            'form': form,  # Передача формы комментария в шаблон
            'year': datetime.now().year,  # Передача текущего года
        }
    )
def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)  # Проверка, что request является объектом HttpRequest

    if request.method == "POST":  # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')  # переадресация на страницу Блог после создания статьи Блога

    else:
        blogform = BlogForm()  # создание объекта формы для ввода данных

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,  # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )
def videopost(request):
    """Renders the videopost page."""
    videos = Video.objects.all()  # Получаем все видео
    return render(
        request,
        'app/videopost.html',
        {
            'videos': videos,  # Передаем список всех видео в шаблон
            'year': datetime.now().year,
        }
    )