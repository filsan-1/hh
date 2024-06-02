from django.contrib import admin
from django.contrib import admin
from .models import Period, Symptom

class SymptomInline(admin.TabularInline):
    model = Symptom
    extra = 1

class PeriodAdmin(admin.ModelAdmin):
    inlines = [SymptomInline]

admin.site.register(Period, PeriodAdmin)
admin.site.register(Symptom)

# Register your models here.
