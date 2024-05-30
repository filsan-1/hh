from django.urls import path
from Home import views

app_name = 'Home'

urlpatterns = [
    path('', views.index, name='home'),
    path('contact', views.contact, name='contact'),
    path('faq', views.faq, name='faq'),
    path('pcod', views.pcod, name='pcod'),
    path('selfcare', views.selfcare, name='selfcare'),
    path('add_period/', views.add_period, name='add_period'),
    path('period_list/', views.period_list, name='period_list'),
    path('period_detail/<int:period_id>/', views.period_detail, name='period_detail'),
    path('add_symptom/<int:period_id>/', views.add_symptom, name='add_symptom'),
]
