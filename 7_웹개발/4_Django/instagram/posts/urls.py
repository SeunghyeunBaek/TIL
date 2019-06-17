from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),  # 전체 글보기 READ
    path('create/', views.create, name='create'),  # 포스트 작성 CREATE
    path('<int:post_id>/update/', views.update, name='update'),  # 포스트 수정 UPDATE
    path('<int:post_id>/delete/', views.delete, name='delete'),  # 포스트 삭제 DELETE

    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create')  # 댓글 생성 CREATE
    # TODO path('<int:post_id>/comment/<int:comment:id>/update/', views_comment_update, name='comment_update')  # 댓글 수정 UPDATE
    # TODO path('<int:post_id>/comment/<int:comment:id>/delete/', views_comment_delete, name='comment_delete')  # 댓글 수정 UPDATE
]
