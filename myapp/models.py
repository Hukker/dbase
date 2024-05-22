from django.db import models
from django.forms import ValidationError
    
class Workers(models.Model):
    STATUS_CHOICES = (
        ('фельдшер', 'фельдшер'),
        ('медсестра', 'медсестра'),
        ('водитель', 'водитель'),
    )
    
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    info = models.ForeignKey('WorkersInfo', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class WorkersInfo(models.Model):
    startwork = models.DateField(max_length=255)
    startsickness = models.DateField(null=True, max_length=255)
    startvacition = models.DateField(null=True, max_length=255)
    endvacition = models.DateField(null=True, max_length=255)
    endsickness = models.DateField(null=True, max_length=255)
    endwork = models.DateField(null=True, max_length=255)


class Brigade(models.Model):
    feldsher = models.ForeignKey(
        Workers,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'status': 'фельдшер'},
        related_name='feldsher_brigades'  # Имя для обратной связи с фельдшерами
    )
    med = models.ForeignKey(
        Workers,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'status': 'медсестра'},
        related_name='med_brigades'  # Имя для обратной связи с медсестрами
    )
    driver = models.ForeignKey(
        Workers,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'status': 'водитель'},
        related_name='driver_brigades'  # Имя для обратной связи с водителями
    )
    
    car = models.ForeignKey('Cars', on_delete=models.DO_NOTHING)
    
    worktimestart = models.TimeField(max_length=255)
    worktimeend = models.TimeField(max_length=255)

    number = models.CharField(max_length=255)

    def __str__(self):
        return self.number



class Report(models.Model):
    RESULTS_CHOICES = (
        ('умер', 'умер'),
        ('везем в больницу', 'везем в больницу'),
        ('оказано лечение', 'оказано лечение'),
    )
    
    symptom = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)
    
    brigade = models.ForeignKey(Brigade, on_delete=models.DO_NOTHING)
    
    result = models.CharField(max_length=255, choices = RESULTS_CHOICES)
    
    timestart = models.TimeField(max_length=255)
    year = models.IntegerField()


class Cars(models.Model):
    TYPES_CHOICES = (
        ('реанимация', 'реанимация'),
        ('обычная', 'обычная'),
    )
    type = models.CharField(max_length=255, choices=TYPES_CHOICES)
    number = models.CharField(max_length=255)
    mark = models.CharField(max_length=255)

    def __str__(self):
        return self.mark
    
class RelutsInsepctions(models.Model):
    person = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    result = models.CharField(max_length=255)
    
    def __str__(self):
        return self.person