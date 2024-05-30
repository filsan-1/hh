from django.db import models
from django.contrib.auth.models import User

class Period(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    cycle_length = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}: {self.start_date} - {self.end_date}"

class Symptom(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    date = models.DateField()
    symptom = models.CharField(max_length=100)
    severity = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.period.user.username}: {self.symptom} on {self.date}"
