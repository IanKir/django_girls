from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from mainpage.models import Task
from mainpage.forms import TaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

    
# TODO Ян делает эту часть проекта
# TODO сделать редирект на signin(войти в систему) and signup(зарегистрироваться)
def task_board_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            tasks = Task.objects.filter(
                published_date__lte=timezone.now()
            ).order_by('published_date')
            return render(
                request=request,
                template_name='mainpage/task_board.html',
                context={'tasks': tasks}
            )
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


# TODO Миша делает эту часть проекта
def main_page(request):

    if request.user.is_authenticated:
        return redirect(to='task_board_page')
    else:
        return render(
            request=request,
            template_name='mainpage/mainpage_template.html'
        )


def user_login_logout(request):

    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == "login_form":
            username = request.POST.get("login")
            if not username:
                return render(
                    request=request,
                    template_name='login/login_template.html',
                    context={"problem_description": "Не указан логин"} )

        if form_type == "password_form":
            password = request.POST.get("password")
            if not password:
                return render(
                    request = request,
                    template_name = 'login/login_template.html',
                    context = {"problem_description": "Не указан пароль"} )
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return render(
                    request=request,
                    template_name='mainpage/task_board.html',
                    context={'tasks': tasks}
                )
            else:
                return render(
                    request=request,
                    template_name='login/login_template.html',
                    context={"problem_description": "Ошибка авторизации"})
            # TODO : залогинить пользователя на task/board если все ок или перекинуть его назад на mainpage если нет

            # TODO: После логина отправить чувака на борду

        elif form_type == "registration_form":
            form = registration_form(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.profile.email = form.cleaned_data.get('email')
                user.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return render(
                    request=request,
                    template_name='mainpage/task_board.html',
                    context={'tasks': tasks}
                )
        else:
            return render(
                request=request,
                template_name='login/login_template.html',
                context={"problem_description": "not supported form exception"})
            # TODO редиректим чувака на главную (ошибка) not supported form exception

    elif request.method == 'GET':
        return render(
            request=request,
            template_name='login/login_template.html'
        )
    else:
        raise Http404("Not supported action 404")
