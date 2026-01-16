from django.urls import path
from . import views

app_name = 'App_Messaging'

urlpatterns = [
    path('messages/', views.conversation_list, name='conversation_list'),
    path('messages/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('messages/start/', views.start_conversation, name='start_conversation'),
    path('messages/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
]
