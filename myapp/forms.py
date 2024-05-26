from dataclasses import fields
import datetime
from django import forms
from .models import *

class WorkersForm(forms.ModelForm):
    worker = forms.ModelChoiceField(queryset=Workers.objects.all().order_by('name'), label='сотрудник')
    # Start date of illness with multiple input formats allowed
    startsickness = forms.DateField(
        label='дата начала болезни', required=False,
        input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']
    )
    # End date of illness with multiple input formats allowed
    endsickness = forms.DateField(
        label='дата окончания болезни', required=False,
        input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']
    )

    class Meta:
        model = WorkerIllness
        fields = ['worker', 'startsickness', 'endsickness']        
        
    def save(self, commit=True):
        # Get the worker instance from cleaned data
        worker = self.cleaned_data['worker']
        # Create a new WorkerIllness instance with the form data
        illness = WorkerIllness(
            startsickness=self.cleaned_data.get('startsickness'),
            endsickness=self.cleaned_data.get('endsickness')
        )

        if commit:
            # Save the WorkerIllness instance
            illness.save()
            # Create a new WorkerHistory entry to link the worker and the illness
            WorkerHistory.objects.create(worker=worker, illness_info=illness)

        return worker


class CarsForm(forms.ModelForm):
    TYPES_CHOICES = (
        ('реанимация', 'реанимация'),
        ('обычная', 'обычная'),
    )
    
    type = forms.ChoiceField(choices=TYPES_CHOICES, label='тип автомобиля')
    number = forms.CharField( label='номер автомобиля')
    mark = forms.CharField(label='марка автомобиля')
    datestart = forms.DateField(
        label='дата принятия',
    )
    dateend = forms.DateField(
        label='дата списания',
        required=False
    )

    class Meta:
        model = Cars
        fields = '__all__'



class ReportForm(forms.ModelForm):
    RESULTS_CHOICES = (
        ('умер', 'умер'),
        ('везем в больницу', 'везем в больницу'),
        ('оказано лечение', 'оказано лечение'),
    )
    
    symptom = forms.CharField(label='симптомы')
    name = forms.CharField(max_length=255, label='имя')
    adress = forms.CharField(max_length=255, label='адресс')
    date = forms.DateField(label='дата исполнения', widget=forms.DateInput(attrs={'type': 'date'}))
    brigade = forms.ModelChoiceField(queryset=Brigade.objects.all().order_by('number'), label='бригада')
    result = forms.ChoiceField(choices=RESULTS_CHOICES, label='диагноз')
    timestart = forms.TimeField(label='Время начала приема', widget=forms.TimeInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Report
        fields = ['date', 'timestart', 'name', 'adress', 'symptom', 'brigade', 'result']