from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),  # 전체 글보기 READ
    path('create/', views.create, name='create'),  # 포스트 작성 CREATE
    path('<int:post_id>/update/', views.update, name='update'),  # 포스트 수정 UPDATE
    path('<int:post_id>/delete/', views.delete, name='delete'),  # 포스트 삭제 DELETE

    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),  # 댓글 생성 CREATE
    path('<int:post_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),  # 댓글 삭제 DELETE
    # TODO path('<int:post_id>/comments/<int:comment:id>/update/', views.comment_update, name='comment_update'),  # 댓글 수정 UPDATE

    path('<int:post_id>/likes/', views.likes, name='likes'),  # on-off 좋아요가 눌려있으면 취소, 안눌려있으면 누름

]
