from django.urls import path
from . import views

app_name = 'Hormonal_Twins'

urlpatterns = [
    path('', views.TwinListView.as_view(), name='twin_list'),
    path('profile/<str:username>/', views.TwinDetailView.as_view(), name='twin_detail'),
    path('create-profile/', views.create_twin_profile, name='create_profile'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('find-matches/', views.find_matches, name='find_matches'),
    path('connect/<int:user_id>/', views.connect_twin, name='connect_twin'),
    path('connections/', views.my_connections, name='my_connections'),
    path('accept/<int:connection_id>/', views.accept_connection, name='accept_connection'),
    path('block/<int:connection_id>/', views.block_connection, name='block_connection'),
]
