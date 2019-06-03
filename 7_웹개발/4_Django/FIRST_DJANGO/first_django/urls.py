from django.contrib import admin
from django.urls import path
from . import views  # 같은 위치의 views import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    # variable routing
    path('hello]/<str:name>/', views.hello),
    ]
