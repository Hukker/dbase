from dataclasses import fields
import datetime
from django import forms
from .models import *
    
class WorkersForm(forms.ModelForm):
    person = forms.ModelChoiceField(queryset=Workers.objects.all().order_by('name'), label='сотрудник')
    startvacition = forms.DateField(
        label='дата начала отпуска', required=False,
        input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']
    )
    endvacition = forms.DateField(
        label='дата окончания отпуска', required=False,
        input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']
    )
    startsickness = forms.DateField(
        label='дата начала болезни', required=False,
        input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']
    )
    endsickness = forms.DateField(
        label='дата окончания болезни', required=False,
        input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']
    )
    endwork = forms.DateField(
        label='дата окончания работы', required=False,
        input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']
    )
    

    class Meta:
        model = WorkersInfo
        fields = ['person', 'startvacition', 'endvacition', 'startsickness', 'endsickness', 'endwork']        
        
    def save(self, commit=True):
        worker = self.cleaned_data['person']
        worker.info.startvacition = self.cleaned_data.get('startvacition')
        worker.info.endvacition = self.cleaned_data.get('endvacition')
        worker.info.startsickness = self.cleaned_data.get('startsickness')
        worker.info.endsickness = self.cleaned_data.get('endsickness')
        worker.info.endwork = self.cleaned_data.get('endwork')

        if commit:
            worker.info.save()
            worker.save()
        
        return worker


class CarsForm(forms.ModelForm):
    TYPES_CHOICES = (
        ('реанимация', 'реанимация'),
        ('обычная', 'обычная'),
    )
    
    type = forms.ChoiceField(choices=TYPES_CHOICES, label='тип автомобиля')
    number = forms.CharField( label='номер автомобиля')
    mark = forms.CharField(label='марка автомобиля')

    class Meta:
        model = Cars
        fields = '__all__'
        

class DeleteCarForm(forms.Form):
    car_id = forms.IntegerField(min_value=1, label='номер автомобиля')
    
    
class BrigadeForm(forms.ModelForm):
    number = forms.ModelChoiceField(queryset=Brigade.objects.all().order_by('number'), label='номер бригады')
    worktimestart = forms.TimeField(label='Время начала приема', widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}))
    worktimeend = forms.TimeField(label='Время конца приема', widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}))


    class Meta:
        model = Brigade
        fields = ['number', 'worktimestart','worktimeend']
        
        
class ReportForm(forms.ModelForm):
    RESULTS_CHOICES = (
        ('умер', 'умер'),
        ('везем в больницу', 'везем в больницу'),
        ('оказано лечение', 'оказано лечение'),
    )
    
    symptom = forms.CharField(label='симптомы')
    name = forms.CharField(max_length=255, label='имя')
    adress = forms.CharField(max_length=255, label='адресс')
    year = forms.IntegerField(label='год исполнения', min_value=1924, max_value=2024)
    brigade = forms.ModelChoiceField(queryset=Brigade.objects.all().order_by('number'), label='бригада')
    result = forms.ChoiceField(choices=RESULTS_CHOICES, label='диагноз')
    timestart = forms.TimeField(label='Время начала приема', widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}))

    class Meta:
        model = Report
        fields = ['name', 'adress', 'symptom', 'brigade', 'result', 'timestart', 'year']