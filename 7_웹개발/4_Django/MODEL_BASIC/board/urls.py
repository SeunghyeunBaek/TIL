from django.urls import path
from . import views

urlpatterns = [
    # Create
    path('article_create/', views.article_create),  # board/article_create
    path('article_save/', views.article_save),  # board/article_save

    # Read
    path('', views.article_list),  # board/
    path('<int:article_id>/', views.article_detail),  # board/article.id

    # Update
    path('article_edit/<int:article_id>/', views.article_edit),  # board/article_edit/article.id
    path('article_update/<int:article_id>/', views.article_update),  # board/article_update/article.id

    # Delete
    path('article_delete/<int:article_id>/', views.article_delete)  # /board/article_delete/article.id
]
