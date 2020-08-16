from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # Read
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail, name='detail'),

    # Create
    # path('new/', views.new, name='new'),  # 새글을 쓰기 위한 form 제공
    path('create/', views.create, name='create'),  # DB에 새글 추가
    path('create_dummies/', views.create_dummies, name='create_dummies'),  # 뻘글 10개 만들기

    # Delete
    path('<int:article_id>/delete/', views.delete, name='delete'),

    # Update
    # path('<int:article_id>/edit/', views.edit, name='edit'),
    path('<int:article_id>/update/', views.update, name='update'),

    # READ_comment
    path('comment_all', views.comment_all, name='comment_all'),

    # CREATE_comment
    # articles/5/comments/create
    path('<int:article_id>/comments/create/', views.create_comment, name='create_comment'),

    # DELETE_comment
    path('<int:article_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment')
    ]
