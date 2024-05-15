from django import forms
from .models import *


class BrigadeForm(forms.ModelForm):
    feldsher = forms.ModelChoiceField(queryset=Feldshers.objects.all(), label='Фельдшер', empty_label='')
    med = forms.ModelChoiceField(queryset=Meds.objects.all(), label='Медик', empty_label='')
    driver = forms.ModelChoiceField(queryset=Drivers.objects.all(), label='Водитель', empty_label='')
    car = forms.ModelChoiceField(queryset=Cars.objects.all(), label='Машина', empty_label='')
    worktimestart = forms.TimeField(label='Время начала приема',widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}))
    worktimeend = forms.TimeField(label='Время конца приема',widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}))
    busy = forms.BooleanField(label='В работе',widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),required=False)
    number = forms.ModelChoiceField(queryset = BrigadeNumber.objects.all(),label = 'номер бригады')

    class Meta:
        model = Brigade
        fields = '__all__'


class FeldshersForm(forms.ModelForm):
    name = forms.CharField(label='Фельдшер')


    class Meta:
        model = Feldshers
        fields = '__all__'


class MedsForm(forms.ModelForm):
    name = forms.CharField( label='Медик')

    class Meta:
        model = Meds
        fields = '__all__'


class DriverForm(forms.ModelForm):
    name = forms.CharField(label='Водитель')

    class Meta:
        model = Drivers
        fields = '__all__'


class ReportForms(forms.ModelForm):
    symptom = forms.CharField(label= 'симптомы')
    name=forms.CharField(max_length=255,label='имя',widget=forms.TextInput(attrs={'class': 'form-control'}))
    adress = forms.CharField(max_length=255,label='адресс')
    brigade = forms.ModelChoiceField(queryset=Brigade.objects.all(),label='бригада')
    result = forms.CharField(max_length=255,label='диагноз')
    year = forms.IntegerField(label ='год рождения', min_value=1924,max_value=2024)

    class Meta:
        model = Report
        fields = '__all__'


class CarsForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=TypeCars.objects.all(),label ='тип автомобиля')
    number = forms.CharField(max_length=255,label='автомобильный номер')
    mark = forms.CharField(max_length=255,label='марка автомобиля')

    class Meta:
        model = Cars
        fields = '__all__'