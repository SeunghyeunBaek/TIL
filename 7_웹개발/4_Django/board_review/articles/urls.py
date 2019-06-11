from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # READ
    path('', views.index, name='index'),  # read all
    path('<int:article_id>/', views.detail, name='detail'),  # read one

    # Create
    path('create/', views.create, name='create'),

    # Update
    path('<int:article_id>/update', views.update, name='update'),

    # Delete
    path('<int:article_id>/delete', views.delete, name='delete'),

    # Create_comment
    path('<int:article_id>/create_comment', views.create_comment, name='create_comment'),

    # Delete_comment
    path('<int:article_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment')

    ]
