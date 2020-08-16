from django.contrib import admin
from django.urls import path, include

# master app 에서는 include 구문으로 url 을 담당하는 app 에 넘긴다.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),  # home/ 으로 시작하는 url 은 home.urls 로 보낸다.
    path('utils/', include('utils.urls')),
    ]
