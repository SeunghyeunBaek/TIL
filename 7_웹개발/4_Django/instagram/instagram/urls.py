from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from posts import views

urlpatterns = [
    path('', views.all),  # 모든 게시글 가져오기
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
