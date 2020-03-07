from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django import views


class MainPageView(views.View):
    def get(self, request):

        if request.user.is_authenticated:

            pass
        else:
            pass

        # data = request.body.decode()
        return render(
            request=request,
            template_name='mainpage/mainpage_template.html'
            # using=str(data)
        )
        # return {"item": data}
    
# TODO Ян делает эту часть проекта
def task_board_page(request):
    pass

# TODO Миша делает эту часть проекта
def main_page(request):

    if request.user.is_authenticated:
        pass # кинуть на борду редиректом

    if request.method == 'POST':        
        form_type = request.POST.get("form_type")

        if form_type == "login_form":
            user_login = request.POST.get("login")
            if not user_login:
                return render(
                    request=request,
                    template_name='mainpage/mainpage_template.html',
                    {"problem_description" : "Не указан лоин"}
                )

            # TODO: достать данные формы

            # TODO : залогинить пользователя в его аккаунт если все ок или перекинуть его назад на главную если нет
            
            # TODO: После логина отправить чувака на борду

        elif form_type == "registration_form":
            # СОздать пользователя в базе (гуглим django create user account)
            pass
        else:

            pass
            # TODO редиректим чувака на главную (ошибка) not supported form exception

    elif request.method == 'GET':
        return render(
            request=request,
            template_name='mainpage/mainpage_template.html'
            # using=str(data)
        )
    else:
        # TODO: Not supported exception (4**?)


def post_list(request):
    posts = (Post.objects.filter(published_date__lte=timezone.now())
             .order_by('published_date'))
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
