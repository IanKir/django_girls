from django.contrib.auth import login, authenticate
from register.forms import SignUpForm
from django.shortcuts import render, redirect


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.profile.telegram = form.cleaned_data.get('Telegram')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(to='task_board_page')
    else:
        form = SignUpForm()
    return render(request, 'register/signup.html', {'form': form})
