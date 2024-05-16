from django.http import HttpResponse
from myapp.models import *
from myapp.forms import *
from itertools import count
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from .forms import *
from .models import *


def index(request):
    return render(request, 'myapp/index.html')

def workers(request):
    objects = Workers.objects.all().order_by('name')
    form = WorkersForm()
    
    if (request.method == 'POST'):
        form = WorkersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Worker saved')
        else:
            messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')
        form = WorkersForm()
        
        
    return render(request, 'myapp/workers.html', {'objects': objects, 'form': form})


def cars(request):
    objects = Cars.objects.all().order_by('number')
    form = CarsForm()
    delete_form = DeleteCarForm()

    if request.method == 'POST':
        if 'add' in request.POST:  # Если отправлена форма добавления
            form = CarsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Машина успешно добавлена')
                return redirect('cars')  # Перенаправляем на страницу снова после успешного добавления
            else:
                messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')

        elif 'delete' in request.POST:  # Если отправлена форма удаления
            delete_form = DeleteCarForm(request.POST)
            if delete_form.is_valid():
                car_id = delete_form.cleaned_data['car_id']
                car = Cars.objects.get(pk=car_id)
                car.delete()
                messages.success(request, 'Машина успешно удалена')
                return redirect('cars')  # Перенаправляем на страницу снова после успешного удаления

    return render(request, 'myapp/cars.html', {'objects': objects, 'form': form, 'delete_form': delete_form})


def brigades(request):
    objects = Brigade.objects.all().order_by('worktimestart')
    form = BrigadeForm()

    if (request.method == 'POST'):
        form = BrigadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brigade saved')
        else:
            messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')
        form = BrigadeForm()
        
        
    return render(request, 'myapp/brigade.html', {'objects': objects, 'form': form})

def reports(request):
    objects = Report.objects.all().order_by('name')
    form = ReportForm

    if (request.method == 'POST'):
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report saved')
        else:
            messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')
        form = ReportForm()
        
    return render(request, 'myapp/reports.html', {'objects': objects, 'form': form})
