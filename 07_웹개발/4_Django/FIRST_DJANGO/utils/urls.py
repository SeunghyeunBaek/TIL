from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('art/<str:keyword>/', views.artii),
    path('stock/', views.stock),
]
