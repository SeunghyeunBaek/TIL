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

    # Delete
    path('<int:article_id>/delete/', views.delete, name='delete'),

    # Update
    # path('<int:article_id>/edit/', views.edit, name='edit'),
    path('<int:article_id>/update/', views.update, name='update'),
    ]
