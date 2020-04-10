from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone

from mainpage.forms import TaskForm
from mainpage.models import Task, Profile


# TODO: @property для модели Task
# TODO: сделать кастомную form для tasks, как для login_form
# TODO: Сделать функционал принять задание, оно потом убирается из общего списка
# todo: добавить возможность снятия задачи с выполнения пользователем, который ее создал
def task_board_page(request):
    """Все задачи, кроме тех, что создал пользователь и которые он выполняет"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            tasks = Task.objects.filter(
                published_date__lte=timezone.now()
            ).exclude(
                author=request.user,
                # fixme: все равно отображает те задачи, которые принял пользователь
                executor=request.user.profile
            ).order_by('published_date')
            return render(
                request=request,
                template_name='mainpage/task_board.html',
                context={'tasks': tasks})
        else:
            return redirect(to='user_login')


def task_board_set(request):
    """Задачи, которые пользователь поставил"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            tasks = Task.objects.filter(
                published_date__lte=timezone.now(),
                author=request.user
            ).order_by('published_date')
            return render(
                request=request,
                template_name='mainpage/task_board.html',
                context={'tasks': tasks})
        else:
            return redirect(to='user_login')


def task_board_performs(request):
    """Задачи, в которых пользователь является исполнителем"""
    if request.user.is_authenticated:
        if request.method == 'GET':
            tasks = Task.objects.filter(
                published_date__lte=timezone.now(),
                executor=request.user.profile
            ).order_by('published_date')
            return render(
                request=request,
                template_name='mainpage/task_board.html',
                context={'tasks': tasks})
    else:
        return redirect(to='user_login')


def accept_task(request, pk):
    """Устанавливает исполнителя задачи"""
    if request.user.is_authenticated:
        # if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        if request.user != task.author:
            task.executor.add(request.user.profile)
            task.save()
        else:
            return render(
                request=request,
                template_name='mainpage/task_detail.html',
                context={'accept_error', 'Вы не можете принять задачу, которую вы создали'}
            )
        return redirect(to='task_board_performs')
    else:
        return redirect(to='user_login')


def task_detail(request, pk):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, pk=pk)
        return render(
            request=request,
            template_name='mainpage/task_detail.html',
            context={'task': task}
        )


def task_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
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
            context={'form': form}
        )


def task_edit(request, pk):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, pk=pk)
        if request.method == "POST":
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
            context={'form': form}
        )


def main_page(request):
    if request.user.is_authenticated:
        return redirect(to='task_board_page')
    else:
        return render(
            request=request,
            template_name='mainpage/greeting.html'
        )


def user_login(request):
    if request.method == 'POST':
        form_type = request.POST.get("form_type")
        if form_type == "sign_in_form":
            username = request.POST.get('username')
            if not username:
                return render(
                    request=request,
                    template_name='login/login_template.html',
                    context={'problem_description1': "Username обязательное поле"}
                )
            password = request.POST.get('password')
            # Зачем проводить проверку пароля, если в форме в login_template я указал это поле обязательным
            # Потому что в html можно указать это поле не обязательным и все поломается
            if not password:
                return render(
                    request=request,
                    template_name='login/login_template.html',
                    context={'problem_description1': "Password обязательное поле"}
                )
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect(to='task_board_page')
            else:
                return render(
                    request=request,
                    template_name='login/login_template.html',
                    context={'problem_description1': 'Ошибка авторизации'}
                )
        elif form_type == "sign_up_form":
            username = request.POST.get('username')
            password = request.POST.get('password1')
            # TODO: Добавить простую проверку на длину пароля
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user = User.objects.create_user(
                username=username,
                password=password)
            user.save()
            profile = Profile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email)
            profile.save()
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
            return redirect(to=task_board_page)
        else:
            return render(
                request=request,
                template_name='login/login_template.html',
                context={"problem_description2": "Not supported form"})
    elif request.method == 'GET':
        return render(
            request=request,
            template_name='login/login_template.html'
        )
    else:
        raise Http404("Not supported action 404")


def user_logout(request):
    logout(request=request)
    return redirect(to='main_page')
