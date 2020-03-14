from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from mainpage.models import Task
from mainpage.forms import TaskForm

    
# TODO Ян делает эту часть проекта
# TODO сделать редирект на signin(войти в систему) and signup(зарегистрироваться)
def task_board_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            tasks = Task.objects.filter(
                published_date__lte=timezone.now(),
                author=request.user
            ).order_by('published_date')
            return render(
                request=request,
                template_name='taskboard/task_board.html',
                context={'tasks': tasks}
            )
        else:
            return redirect(to='main_page')


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'taskboard/task_detail.html', {'task': task})


def task_new(request):
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
    return render(request, 'taskboard/task_edit.html', {'form': form})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.published_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'taskboard/task_edit.html', {'form': form})


# TODO Миша делает эту часть проекта
def main_page(request):

    if request.user.is_authenticated:
        return redirect(to='task_board_page')

    if request.method == 'POST':        
        form_type = request.POST.get("form_type")
        # add_authenticate
        if form_type == "login_form":
            user_login = request.POST.get("login")
            if not user_login:
                return render(
                    request=request,
                    template_name='mainpage/mainpage_template.html',
                    context={"problem_description": "Не указан логин"}
                )

            # TODO: достать данные формы

            # TODO : залогинить пользователя в его аккаунт если все ок или перекинуть его назад на главную если нет
            
            # TODO: После логина отправить чувака на борду

        elif form_type == "registration_form":
            # Создать пользователя в базе (гуглим django create user account)
            pass
        else:
            pass
            # TODO редиректим чувака на главную (ошибка) not supported form exception

    elif request.method == 'GET':
        return render(
            request=request,
            template_name='mainpage/mainpage_template.html'
        )
    else:
        # Эта ошибка выведится в консоль, нужно сделать ошибку Django
        raise Exception("Not supported exception 4**?")
