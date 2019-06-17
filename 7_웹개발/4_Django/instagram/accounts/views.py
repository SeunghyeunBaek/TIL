from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def signup(request):
    if request.user.is_authenticated:  # 이미 로그인 했다면
        return redirect('posts:index')
    else:
        if request.method == 'POST':
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)  # 회원가입 후 바로 로그인
                return redirect('posts:index')
            else:
                pass
        else:
            form = UserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:  # 이미 로그인 했다면
        return redirect('posts:index')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            print(form)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect('posts:index')
            else:
                pass
        else:
            form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('posts:index')


