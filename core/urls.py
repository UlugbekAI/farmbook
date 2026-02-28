from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('issues/', views.issue_list, name='issues'),
    path('plant-protection/', views.product_list, {'group': 'protection'}, name='plant_protection'),
    path('fertilizers/', views.product_list, {'group': 'fertilizer'}, name='fertilizers'),
    path('irrigation/', views.irrigation_list, name='irrigation'),
    path('sprays/', views.spray_list, name='sprays'),
]
