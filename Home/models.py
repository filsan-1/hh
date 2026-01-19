from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Period(models.Model):
    FLOW_CHOICES = [
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
        ('spotting', 'Spotting'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    cycle_length = models.IntegerField(default=28)
    flow = models.CharField(max_length=10, choices=FLOW_CHOICES, default='medium')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.username}: {self.start_date} - {self.end_date or 'ongoing'}"
    
    def get_duration(self):
        """Calculate period duration in days"""
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None
    
    def predict_next_period(self):
        """Predict next period start date based on cycle length"""
        if self.start_date and self.cycle_length:
            return self.start_date + timedelta(days=self.cycle_length)
        return None

class Symptom(models.Model):
    SYMPTOM_CATEGORIES = [
        ('cramps', 'Cramps/Pain'),
        ('headache', 'Headache'),
        ('bloating', 'Bloating'),
        ('fatigue', 'Fatigue'),
        ('nausea', 'Nausea'),
        ('backache', 'Back Pain'),
        ('breast_tenderness', 'Breast Tenderness'),
        ('mood_swings', 'Mood Swings'),
        ('acne', 'Acne/Skin Issues'),
        ('cravings', 'Food Cravings'),
        ('insomnia', 'Sleep Issues'),
        ('diarrhea', 'Digestive Issues'),
        ('other', 'Other'),
    ]
    
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('sad', '😢 Sad'),
        ('anxious', '😰 Anxious'),
        ('irritable', '😤 Irritable'),
        ('tired', '😴 Tired'),
        ('energetic', '⚡ Energetic'),
        ('normal', '😐 Normal'),
    ]
    
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    date = models.DateField()
    symptom_type = models.CharField(max_length=30, choices=SYMPTOM_CATEGORIES)
    severity = models.IntegerField(help_text="Rate from 1 (mild) to 10 (severe)")
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.period.user.username}: {self.get_symptom_type_display()} ({self.severity}/10) on {self.date}"
