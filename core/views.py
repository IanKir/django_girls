"""Модуль обработки запросов от пользователя."""
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import DatabaseError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from core.forms import TaskForm
from core.models import Task, Profile


# TODO: сделать кастомную form для tasks, как для login_form
# todo: добавить возможность снятия задачи
#  с выполнения пользователем, который ее создал

def get_tasks_paginator(tasks, pages_quantity, page):
    """Выполняет пагинацию запроса из БД.

    Arguments:
        tasks: задачи из БД
        pages_quantity: количнство страниц для пагинации
        page: номер страницы из запроса клиента

    Return:
        tasks: задачи после пагинации
    """
    paginator = Paginator(tasks, pages_quantity)

    try:
        tasks = paginator.get_page(page)
    except PageNotAnInteger:
        tasks = paginator.get_page(1)
    except EmptyPage:
        tasks = paginator.get_page(paginator.num_pages)

    return tasks


def task_board_page(request):
    """Все задачи, кроме тех, что создал пользователь и которые он выполняет.

    Arguments:
        request: запрос от клиента

    Returns:
        render(): рендер страницы mainpage/task_board.html
        с задачами из базы, которые пользователь может выполнить

        redirect(): редирект пользователя на страницу регистрации,
        если он не зарегистрирован
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            page = request.GET.get('page')
            try:
                tasks = Task.objects.filter(
                    published_date__lte=timezone.now(),
                ).exclude(
                    author=request.user,
                ).exclude(
                    executor=request.user.profile,
                ).order_by('published_date')
            except DatabaseError:
                tasks = {}

            tasks_to_response = get_tasks_paginator(
                tasks=tasks,
                pages_quantity=7,
                page=page,
            )
            return render(
                request=request,
                template_name='mainpage/task_board.html',
                context={
                    'tasks': tasks_to_response,
                    'which_func': 'task_board_page',
                },
            )
        return redirect(to='user_login')


def task_board_set(request):
    """Задачи, которые пользователь поставил.

    Arguments:
        request: запрос от клиента

    Returns:
        render(): рендер страницы mainpage/task_board.html
        с задачами из базы, которые пользователь создал

        redirect(): редирект пользователя на страницу регистрации,
        если он не зарегистрирован
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            page = request.GET.get('page')
            try:
                tasks = Task.objects.filter(
                    published_date__lte=timezone.now(),
                    author=request.user,
                ).order_by('published_date')
            except DatabaseError:
                tasks = {}

            tasks_to_response = get_tasks_paginator(
                tasks=tasks,
                pages_quantity=7,
                page=page,
            )
            return render(
                request=request,
                template_name='mainpage/task_board.html',
                context={
                    'tasks': tasks_to_response,
                    'which_func': 'task_board_set',
                },
            )
        return redirect(to='user_login')


def task_board_performs(request):
    """Задачи, в которых пользователь является исполнителем.

    Arguments:
        request: запрос от клиента

    Returns:
        render(): рендер страницы mainpage/task_board.html
        с задачами из базы, которые пользователь выполняет

        redirect(): редирект пользователя на страницу регистрации,
        если он не зарегистрирован
    """
    if request.user.is_authenticated:
        if request.method == 'GET':
            page = request.GET.get('page')
            try:
                tasks = Task.objects.filter(
                    published_date__lte=timezone.now(),
                    executor=request.user.profile,
                ).order_by('published_date')
            except DatabaseError:
                tasks = {}

            tasks_to_response = get_tasks_paginator(
                tasks=tasks,
                pages_quantity=7,
                page=page,
            )
            return render(
                request=request,
                template_name='mainpage/task_board.html',
                context={
                    'tasks': tasks_to_response,
                    'which_func': 'task_board_performs',
                },
            )
    return redirect(to='user_login')


def accept_task(request, pk):
    """Устанавливает исполнителя задачи.

    Arguments:
        request: запрос от клиента
        pk: primary key(id) для задачи(task)

    Returns:
        redirect(): редирект пользователь на страницу с задачи,
        которые пользователь выполняет

        redirect(): редирект пользователя на страницу регистрации,
        если он не зарегистрирован

        render(): рендер страницы с задачей с ошибкой 'accept_error',
        если пользователь эту задачу ставил
    """
    if request.user.is_authenticated:
        task = get_object_or_404(Task, pk=pk)
        if request.user is not task.author:
            task.executor.add(request.user.profile)
            task.save()
        else:
            error_string = 'Вы не можете принять задачу, которую вы создали'
            return render(
                request=request,
                template_name='mainpage/task_detail.html',
                context={
                    'accept_error': error_string,
                },
            )
        return redirect(to='task_board_performs')
    return redirect(to='user_login')


def task_detail(request, pk):
    """Детальная информация о задаче.

    Arguments:
        request: запрос от клиента
        pk: primary key(id) для задачи(task)

    Returns:
        render(): рендер страницы с детальной информацией,
        одной задачи

        redirect(): редирект пользователя на страницу регистрации,
        если он не зарегистрирован
    """
    if request.user.is_authenticated:
        task = get_object_or_404(Task, pk=pk)
        return render(
            request=request,
            template_name='mainpage/task_detail.html',
            context={'task': task},
        )
    return redirect(to='user_login')


def task_new(request):
    """Создание новой задачи в БД.

    Arguments:
        request: запрос от клиента

    Returns:
        redirect(): если POST-запрос, то создание новой задачи
        в БД и редирект на страницу с детальной информацией этой задачи

        render(): если GET-запрос, то рендер страницы
        с пустой формой для создание новой задачи

        redirect(): редирект пользователя на страницу регистрации,
        если он не зарегистрирован
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.author = request.user
                task.published_date = timezone.now()
                task.save()
                return redirect('task_detail', pk=task.pk)
        else:
            form = TaskForm()
            return render(
                request=request,
                template_name='mainpage/task_edit.html',
                context={'form': form},
            )
    return redirect(to='user_login')


def task_edit(request, pk):
    """Редактировать информацию о задаче.

    Arguments:
        request: запрос от клиента
        pk: primary key(id) для задачи(task)

    Returns:
        redirect(): если POST-запрос, то перезапись информации о задаче
        в БД и редирект на страницу с детальной информацией этой задачи

        render(): если GET-запрос, то рендер страницы
        с заполненной формой для редактирования задачи

        redirect(): редирект пользователя на страницу регистрации,
        если он не зарегистрирован
    """
    if request.user.is_authenticated:
        task = get_object_or_404(Task, pk=pk)
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                task.author = request.user
                task.published_date = timezone.now()
                task.save()
                return redirect(to='task_detail', pk=task.pk)
        else:
            form = TaskForm(instance=task)
            return render(
                request=request,
                template_name='mainpage/task_edit.html',
                context={'form': form},
            )
    return redirect(to='user_login')


def main_page(request):
    """Рендер приветствующей страницы.

    Arguments:
        request: запрос от клиента

    Returns:
        redirect(): если пользователь авторизован, то редирект
        на страницу со списком задач

        render(): если пользователь не авторизован, то рендер
        приветствующей страницы
    """
    if request.user.is_authenticated:
        return redirect(to='task_board_page')
    return render(
        request=request,
        template_name='mainpage/greeting.html',
    )


@require_http_methods(['GET', 'POST'])
def sign_in_user(request):
    """Логин пользователя.

    Arguments:
        request: запрос от клиента

    Returns:
        render(): если поле username пустое, то рендер страницы
        user_sign_in с ошибкой 'username обязательное поле'

        render(): если поле password пустое, то рендер страницы
        user_sign_in с ошибкой 'password обязательное поле'

        redirect(): если пользователь есть в БД то редирект
        на страницу task_board_page

        render(): если пользователь есть в БД, но что-то пошло не так,
        то рендер страницы user_sign_in с ошибкой 'Ошибка авторизации'

        render(): если GET-запрос, то рендер страницы user_sign_in с
        пустыми полями
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username:
            return render(
                request=request,
                template_name='login/user_sign_in.html',
                context={'problem_description': 'Username обязательное поле'},
            )
        if not password:
            return render(
                request=request,
                template_name='login/user_sign_in.html',
                context={'problem_description': 'Password обязательное поле'},
            )
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect(to='task_board_page')
        return render(
            request=request,
            template_name='login/user_sign_in.html',
            context={'problem_description': 'Ошибка авторизации'},
        )
    elif request.method == 'GET':
        return render(
            request=request,
            template_name='login/user_sign_in.html',
        )


def collect_request_values(request):
    """Сбор значений которые передал пользователь.

    Чтобы пользователь не ругался каждый раз, регистируется
    на нашем сервисе, придуман механизм сбора данных, что он отправил
    кроме пароля и потом подставка их в формы, если произошла
    ошибка при регистрации

    Arguments:
         request: запрос клиента

    Returns:
        default_values_into_form: dict с значениями, для подстановки
        в форму регистрации, пароль и csrf-токен, не подставляются
    """
    return {
        field_name: field_value for (field_name, field_value)
        in request.POST.items()
        if field_name != 'csrfmiddlewaretoken'
    }


@require_http_methods(['GET', 'POST'])
def sign_up_user(request):
    """Регистрация пользователя.

    Arguments:
        request: запрос от клиента

    Returns:
        render(): если password < n, то рендер страницы
        user_sign_up с ошибкой 'Пароль должен быть длиннее n символов'

        render(): если попытка создать нового пользователя
        не удалась, то рендер страницы user_sign_up
        с ошибкой 'такой пользователь уже существует или
        ошибка БД'

        redirect(): если создать нового пользователя удалось,
        то редирект на страницу task_board_page

        render(): если GET-запрос, то рендер страницы user_sign_up
        с пустыми полями
    """
    if request.method == 'POST':
        request_values = collect_request_values(request)
        password = request_values.get('password')
        required_password_len = 6
        if password and (len(password) < required_password_len):
            return render(
                request=request,
                template_name='login/user_sign_up.html',
                context={
                    'problem_description': (
                            'Пароль должен быть длиннее ' +
                            '{0} символов'.format(required_password_len)
                    ),
                    **request_values,
                },
            )
        try:
            user = User.objects.create_user(
                username=request_values.get('username'),
                password=request_values.get('password'),
                first_name=request_values.get('first_name'),
                last_name=request_values.get('last_name'),
                email=request_values.get('email'),
            )
        except DatabaseError as data_base_error:
            return render(
                request=request,
                template_name='login/user_sign_up.html',
                context={
                    'problem_description': (
                        'Такой пользователь уже существует ' +
                        'или {0}'.format(str(data_base_error)),
                    ),
                },
            )
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        print(user.username, user.password)
        user = authenticate(
            username=request_values.get('username'),
            password=request_values.get('password')
        )
        if user and user.is_active:
            login(request, user)
            return redirect(to='task_board_page')
        return render(
            request=request,
            template_name='login/user_sign_up.html',
            context={'problem_description': 'Ошибка авторизации'},
        )
    elif request.method == 'GET':
        return render(
            request=request,
            template_name='login/user_sign_up.html',
        )


def user_logout(request):
    """Завершение текущей сессии пользователя.

    Arguments:
        request: запрос клиента

    Returns:
        redirect(): после завершения сессии редирект пользователя
        на страницу main_page
    """
    logout(request=request)
    return redirect(to='main_page')
