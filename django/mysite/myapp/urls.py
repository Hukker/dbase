from . import views

from django.urls import path

urlpatterns = [
    path('index', views.index, name='home'),
    path('', views.index, name='home'),
    path('meds', views.meds, name='meds'),
    path('feldshers', views.feldshers, name='feldshers'),
    path('drivers', views.drivers, name='drivers'),
    path('brigades', views.brigades, name='brigade'),
    path('reports', views.reports, name='reports'),
    path('cars', views.cars, name='cars'),
]

