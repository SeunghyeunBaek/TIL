from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('<int:user_id>/', views.user_page, name='user_page'),  # user_page
    path('<int:user_id>/follow/', views.follow, name='follow')  # follow
]
