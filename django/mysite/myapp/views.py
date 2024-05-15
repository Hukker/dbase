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

def meds(request):
    objects = Meds.objects.all().order_by('name')
    form = MedsForm()
    if(request.method == 'POST'):
        form = MedsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meds saved')
        else:
            messages.error(request, form.errors)
        form = MedsForm()
    return render(request, 'myapp/meds.html', {'objects': objects, 'form': form})


def feldshers(request):
    objects = Feldshers.objects.all().order_by('name')
    form = FeldshersForm()
    if (request.method == 'POST'):
        form = FeldshersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feldsher saved')
        else:
            messages.error(request, form.errors)
        form = FeldshersForm()
    return render(request, 'myapp/feldshers.html', {'objects': objects, 'form': form})

def brigades(request):
    objects = Brigade.objects.all().order_by('busy')
    form = BrigadeForm()

    if (request.method == 'POST'):
        form = BrigadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brigade saved')
        else:
            messages.error(request, form.errors)
        form = BrigadeForm()
    return render(request, 'myapp/brigade.html', {'objects': objects, 'form': form})

def reports(request):
    objects = Report.objects.all().order_by('name')
    form = ReportForms

    if (request.method == 'POST'):
        form = ReportForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report saved')
        else:
            messages.error(request, form.errors)
        form = ReportForms()
    return render(request, 'myapp/reports.html', {'objects': objects, 'form': form})

def cars(request):
    objects = Cars.objects.all().order_by('number')
    form = CarsForm()

    if (request.method == 'POST'):
        form = CarsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car saved')
        else:
            messages.error(request, form.errors)
        form = CarsForm()
    return render(request, 'myapp/cars.html', {'objects': objects, 'form': form})

def drivers(request):
    objects = Drivers.objects.all().order_by('name')
    form = DriverForm()

    if (request.method == 'POST'):
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver saved')
        else:
            messages.error(request, form.errors)
        form = DriverForm()
    return render(request, 'myapp/drivers.html', {'objects': objects, 'form': form})