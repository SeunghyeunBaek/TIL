from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # home/
    path('contact/', views.contact),  # home/contact
    path('help_me/', views.help_me),  # home/help_me
]
