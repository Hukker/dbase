from . import views
from .views import get_brigades


from django.urls import path

urlpatterns = [
    path('index', views.index, name='home'),
    path('', views.index, name='home'),
    path('workers', views.workers, name='meds'),
    path('brigades', views.brigades, name='brigade'),
    path('reports', views.reports, name='reports'),
    path('cars', views.cars, name='cars'),
    path('statistics', views.statistics, name='badbrigades'),
    path('all_workers_illness_history', views.all_workers_illness_history, name='all_workers_illness_history'),
    path('fill', views.fill, name='fill'),
    path('get_brigades/', get_brigades, name='get_brigades'),
]   

