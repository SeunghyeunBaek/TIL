from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'introduce']  # password 는 자동으로 생성, password 쓰면 두번 생성함


class CustomUserChangeForm(UserChangeForm):
    password = None  # 비밀번호 칸 제거, 덮어씌우기

    class Meta:
        model = User
        fields = ['username', 'email', 'introduce', 'image']


