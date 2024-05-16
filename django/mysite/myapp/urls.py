from . import views

from django.urls import path

urlpatterns = [
    path('index', views.index, name='home'),
    path('', views.index, name='home'),
    path('workers', views.workers, name='meds'),
    path('brigades', views.brigades, name='brigade'),
    path('reports', views.reports, name='reports'),
    path('cars', views.cars, name='cars'),
]

