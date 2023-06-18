from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='visual-i-ching-app-home'),
    path('about/', views.about, name='visual-i-ching-app-about')
]
