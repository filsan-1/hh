from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import ContactForm, PeriodForm, SymptomForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Period, Symptom
from datetime import datetime, timedelta
from django.db.models import Avg, Count
from django.contrib import messages

def index(request):
    return render(request, 'Home/home.html')

def faq(request):
    return render(request, 'Home/faq.html')

def pcod(request):
    return render(request, 'Home/pcod.html')

def selfcare(request):
    return render(request, 'Home/selfcare.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("Home:home")
    else:
        form = ContactForm()
    return render(request, "Home/contact.html", {'form': form})

@login_required
def add_period(request):
    if request.method == 'POST':
        form = PeriodForm(request.POST)
        if form.is_valid():
            period = form.save(commit=False)
            period.user = request.user
            period.save()
            messages.success(request, '✅ Period record added successfully!')
            return redirect('Home:period_list')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = PeriodForm()
    return render(request, 'Home/add_period.html', {'form': form})

@login_required
def period_list(request):
    periods = Period.objects.filter(user=request.user).order_by('-start_date')
    
    # Calculate statistics
    context = {
        'periods': periods,
    }
    
    if periods.exists():
        # Calculate average cycle length
        avg_cycle = periods.aggregate(Avg('cycle_length'))['cycle_length__avg']
        context['avg_cycle'] = round(avg_cycle, 1) if avg_cycle else None
        
        # Get next predicted period
        latest_period = periods.first()
        if latest_period:
            predicted_date = latest_period.predict_next_period()
            context['predicted_next'] = predicted_date
            if predicted_date:
                days_until = (predicted_date - datetime.now().date()).days
                context['days_until_next'] = days_until
        
        # Count total symptoms
        total_symptoms = Symptom.objects.filter(period__user=request.user).count()
        context['total_symptoms'] = total_symptoms
    
    return render(request, 'Home/period_list.html', context)

@login_required
def period_detail(request, period_id):
    period = get_object_or_404(Period, id=period_id, user=request.user)
    symptoms = period.symptom_set.all()
    
    # Group symptoms by type for better visualization
    symptom_summary = symptoms.values('symptom_type').annotate(
        count=Count('id'),
        avg_severity=Avg('severity')
    ).order_by('-count')
    
    context = {
        'period': period,
        'symptoms': symptoms,
        'symptom_summary': symptom_summary,
        'duration': period.get_duration(),
    }
    
    return render(request, 'Home/period_detail.html', context)

@login_required
def add_symptom(request, period_id):
    period = get_object_or_404(Period, id=period_id, user=request.user)
    
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom = form.save(commit=False)
            symptom.period = period
            symptom.save()
            messages.success(request, '✅ Symptom logged successfully!')
            return redirect('Home:period_detail', period_id=period.id)
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        # Pre-fill the date with today's date
        form = SymptomForm(initial={'date': datetime.now().date()})
    
    context = {
        'form': form,
        'period': period,
    }
    return render(request, 'Home/add_symptom.html', context)

@login_required
def edit_period(request, period_id):
    period = get_object_or_404(Period, id=period_id, user=request.user)
    
    if request.method == 'POST':
        form = PeriodForm(request.POST, instance=period)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Period updated successfully!')
            return redirect('Home:period_detail', period_id=period.id)
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = PeriodForm(instance=period)
    
    context = {
        'form': form,
        'period': period,
    }
    return render(request, 'Home/edit_period.html', context)

@login_required
def delete_period(request, period_id):
    period = get_object_or_404(Period, id=period_id, user=request.user)
    
    if request.method == 'POST':
        period.delete()
        messages.success(request, '✅ Period deleted successfully!')
        return redirect('Home:period_list')
    
    return render(request, 'Home/delete_period.html', {'period': period})

@login_required
def delete_symptom(request, symptom_id):
    symptom = get_object_or_404(Symptom, id=symptom_id, period__user=request.user)
    period_id = symptom.period.id
    
    if request.method == 'POST':
        symptom.delete()
        messages.success(request, '✅ Symptom deleted successfully!')
        return redirect('Home:period_detail', period_id=period_id)
    
    return render(request, 'Home/delete_symptom.html', {'symptom': symptom})
