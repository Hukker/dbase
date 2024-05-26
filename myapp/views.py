from django.http import HttpResponse
from myapp.models import *
from myapp.forms import *
from itertools import count
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from .forms import *
from .models import *
from .fill import *
from datetime import datetime


def index(request):
    return render(request, 'myapp/index.html')

def workers(request):
    objects = Workers.objects.all().order_by('name')
        
        
    return render(request, 'myapp/workers.html', {'objects': objects})


def cars(request):
    objects = Cars.objects.all().order_by('id')
    form = CarsForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':  # Если отправлена форма добавления
            form = CarsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Машина успешно добавлена')
                return redirect('cars')  # Перенаправляем на страницу снова после успешного добавления
            else:
                messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')


    return render(request, 'myapp/cars.html', {'objects': objects, 'form': form})

def brigades(request):
    objects = Brigade.objects.all().order_by('worktimestart')
    form = BrigadeForm()
    search_query = request.GET.get('search', '')

    if search_query:
        try:
            # Attempt to parse the search query as a time
            search_time = datetime.strptime(search_query, '%H:%M').time()
            objects = objects.filter(
                Q(worktimestart__lte=search_time) & Q(worktimeend__gte=search_time)
            )
        except ValueError:
            pass  # If the search query is not in the correct format, don't filter

    if (request.method == 'POST'):
        form = BrigadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brigade saved')
        else:
            messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')
        form = BrigadeForm()
        
        
    return render(request, 'myapp/brigade.html', {'objects': objects, 'form': form, 'search_query': search_query})

def reports(request):
    objects = Report.objects.all().order_by('date')
    form = ReportForm()
    search_query = request.GET.get('search', '')

    if search_query:
        objects = objects.filter(
            Q(date__icontains=search_query)
        )


    if (request.method == 'POST'):
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report saved')
        else:
            messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')
        form = ReportForm()
        
    return render(request, 'myapp/reports.html', {'objects': objects, 'form': form, 'search_query': search_query,})


def statistics(request):
    objects = Brigade.objects.annotate(
        death_calls_count=Count('report', filter=Q(report__result='умер')),
    ).order_by('worktimestart')
    
    
    
    search_query = request.GET.get('search', '')

    if search_query:
        objects = objects.filter(
            Q(death_calls_count=search_query)
        )
        
    return render(request, 'myapp/statistics.html', {'objects': objects, 'search_query': search_query})

def all_workers_illness_history(request):
    
    objects = WorkerHistory.objects.all().order_by('worker__name')

    form = WorkersForm()
    
    if (request.method == 'POST'):
        form = WorkersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Worker saved')
        else:
            messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')
        form = WorkersForm()
        
    return render(request, 'myapp/all_workers_illness_history.html', {'objects': objects, 'form': form})


def fill(request):
    data = Data()
    data.main()
    return render(request, 'myapp/index.html')