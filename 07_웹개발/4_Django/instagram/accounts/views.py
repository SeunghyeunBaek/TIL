from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .models import User


def signup(request):
    if request.user.is_authenticated:  # 이미 로그인 했다면
        return redirect('posts:index')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)  # 회원가입 후 바로 로그인
                return redirect('posts:index')
            else:
                pass
        else:
            form = CustomUserCreationForm()
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


@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:index')


@login_required
def user_page(request, user_id):
    user_selected = User.objects.get(id=user_id)
    context = {
        'user_selected': user_selected
    }
    return render(request, 'accounts/user_page.html', context)


@login_required
def follow(request, user_id):
    user_following = request.user  # 팔로우를 누르는 유저, username
    user_followed = User.objects.get(id=user_id)  # 팔로우 당하는 유저

    if user_following != user_followed:
        # if user_followed in user_following.follow.all():
        #     # 이미 팔로우를 했다면 팔로우 취소
        #     user_following.follow.remove(user_followed)
        # else:
        #     # 이미 팔로우를 안헀으면 팔로워에 추가
        #     user_following.follow.add(user_followed)

        if user_following in user_followed.follower.all():
            user_followed.follower.remove(user_following)
        else:
            user_followed.follower.add(user_following)
    else:
        pass
    return redirect('accounts:user_page', user_id)


@login_required
def update(request, user_id):
    user_selected = User.objects.get(id=user_id)
    if request.user == user_selected:  # 로그인 한 사람과 수정하려는 사람이 같을 때
        if request.method == 'POST':
            form = CustomUserChangeForm(data=request.POST, files=request.FILES, instance=user_selected)
            if form.is_valid():
                form.save()
                return redirect('accounts:user_page', user_id)
            else:
                pass
        else:
            form = CustomUserChangeForm(instance=user_selected)
        context = {
            'form': form,
            'user_selected': user_selected,
        }
        return render(request, 'accounts/update.html', context)
    else:
        # 로그인 한 사람과 수정하려는 사람이 같지 않을 경우 index 페이지 리턴
        return redirect('accounts:user_page', user_id)
