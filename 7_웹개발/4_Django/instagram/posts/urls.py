from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),  # 전체 글보기 READ
    path('create/', views.create, name='create'),  # 포스트 작성 CREATE
    path('<int:post_id>/update/', views.update, name='update'),  # 포스트 수정 UPDATE
    path('<int:post_id>/delete/', views.delete, name='delete'),  # 포스트 삭제 DELETE

]


