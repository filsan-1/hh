from django.db import models
from django.db import models
from django.contrib.auth.models import User

class PeriodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    cycle_length = models.IntegerField()

class SymptomLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    symptom = models.CharField(max_length=100)
    severity = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    notes = models.TextField(blank=True, null=True)


# Create your models here.
