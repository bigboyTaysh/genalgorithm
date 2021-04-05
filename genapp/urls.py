from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('selection/', views.selection, name='selection'),
    path('crossover/', views.crossover, name='crossover'),
    path('evolution/', views.evolution, name='evolution'),
    path('test/', views.test, name='test'),
    path('lab02/', views.lab02, name='lab02'),
    path('lab03/', views.lab03, name='lab03'),
    path('lab04/', views.lab04, name='lab04'),
    path('lab05/', views.lab05, name='lab05'),
]