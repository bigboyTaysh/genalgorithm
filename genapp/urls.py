from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('lab02/', views.lab02, name='lab02'),
    path('lab03/', views.lab03, name='lab03'),
]