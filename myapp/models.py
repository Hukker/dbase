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

    startwork = models.DateField()

    endwork = models.DateField(null=True)

    def __str__(self):
        return self.name

class WorkerIllness(models.Model):

    startsickness = models.DateField()

    endsickness = models.DateField(null=True)

class WorkerHistory(models.Model):
    worker = models.ForeignKey(Workers, on_delete=models.DO_NOTHING)
    illness_info = models.ForeignKey(WorkerIllness, on_delete=models.CASCADE)


    def __str__(self):
        return self.worker.name


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

    number = models.CharField(max_length=255, unique=True)

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
    date = models.DateField(max_length=255)


class Cars(models.Model):
    TYPES_CHOICES = (
        ('реанимация', 'реанимация'),
        ('обычная', 'обычная'),
    )
    type = models.CharField(max_length=255, choices=TYPES_CHOICES)
    number = models.CharField(max_length=255)
    mark = models.CharField(max_length=255)
    datestart = models.DateField(max_length=255)
    dateend = models.DateField(max_length=255, null=True)
    

    def __str__(self):
        return self.mark
    
class RelutsInsepctions(models.Model):
    person = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    result = models.CharField(max_length=255)
    
    def __str__(self):
        return self.person