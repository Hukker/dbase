from django.db import models
from django.forms import ValidationError

class Feldshers(models.Model):
    name = models.CharField(max_length=255, null=True)
    def __str__(self):
        return f"{self.name} "

class Meds(models.Model):
    name = models.CharField(max_length=255, null=True)
    def __str__(self):
        return f"{self.name} "

class Drivers(models.Model):
    name = models.CharField(max_length=255, null=True)
    def __str__(self):
        return str(self.name)


class BrigadeNumber(models.Model):
    number = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.number


class Brigade(models.Model):
   feldsher = models.ForeignKey(Feldshers, on_delete=models.DO_NOTHING, null=True)
   med = models.ForeignKey(Meds, on_delete=models.DO_NOTHING, null=True)
   driver = models.ForeignKey(Drivers, on_delete=models.DO_NOTHING, null=True)
   car = models.ForeignKey('Cars', on_delete=models.DO_NOTHING, null=True)
   worktimestart = models.CharField(max_length=255, null=True)
   worktimeend = models.CharField(max_length=255, null=True)
   busy = models.BooleanField(default=False)
   number = models.ForeignKey(BrigadeNumber, on_delete=models.DO_NOTHING, null=True)

   def __str__(self):
       return str(self.driver)


class Report(models.Model):
   symptom = models.CharField(max_length=255, null=True)
   name = models.CharField(max_length=255, null=True)
   adress = models.CharField(max_length=255, null=True)
   brigade = models.ForeignKey(BrigadeNumber, on_delete=models.DO_NOTHING, null=True)
   result = models.CharField(max_length=255, null=True)
   year = models.CharField(max_length=255, null=True)


class Cars(models.Model):
    type = models.ForeignKey('TypeCars', on_delete=models.DO_NOTHING)
    number = models.CharField(max_length=255)
    mark = models.CharField(max_length=255)


class TypeCars(models.Model):
    type=models.CharField(max_length=255)
    def __str__(self):
        return self.type




