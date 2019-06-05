from django.contrib import admin
from .models import Article

admin.site.register(Article)

'''
1. python manage.py migrate : 모든 숨겨진 결재 실행
2. python manage.py createsuperuser : 절대관리자를 생성
3. domain/admin 에 접속
4. login
'''