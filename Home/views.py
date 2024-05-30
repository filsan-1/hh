from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import ContactForm, PeriodForm, SymptomForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Period, Symptom

# Views for rendering templates
def index(request):
    return render(request, 'Home/home.html')

def faq(request):
    return render(request, 'Home/faq.html')

def pcod(request):
    return render(request, 'Home/pcod.html')

def selfcare(request):
    return render(request, 'Home/selfcare.html')

class HomeView(ListView):
    template_name = 'Home/home.html'

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

# Views for period-related functionalities
@login_required
def add_period(request):
    if request.method == 'POST':
        form = PeriodForm(request.POST)
        if form.is_valid():
            period = form.save(commit=False)
            period.user = request.user
            period.save()
            return redirect('Home:period_list')
    else:
        form = PeriodForm()
    return render(request, 'Home/add_period.html', {'form': form})

@login_required
def period_list(request):
    periods = Period.objects.filter(user=request.user)
    return render(request, 'Home/period_list.html', {'periods': periods})

@login_required
def period_detail(request, period_id):
    period = get_object_or_404(Period, id=period_id)
    return render(request, 'Home/period_detail.html', {'period': period})

# Views for symptom-related functionalities
@login_required
def add_symptom(request, period_id):
    period = get_object_or_404(Period, id=period_id)
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom = form.save(commit=False)
            symptom.period = period
            symptom.save()
            return redirect('Home:period_detail', period_id=period.id)
    else:
        form = SymptomForm()
    return render(request, 'Home/add_symptom.html', {'form': form})
