from django.urls import path
from . import views

app_name = 'Support_Circle'

urlpatterns = [
    path('', views.CircleListView.as_view(), name='circle_list'),
    path('circle/<int:pk>/', views.CircleDetailView.as_view(), name='circle_detail'),
    path('create/', views.create_circle, name='create_circle'),
    path('edit/<int:pk>/', views.edit_circle, name='edit_circle'),
    path('join/<int:pk>/', views.join_circle, name='join_circle'),
    path('leave/<int:pk>/', views.leave_circle, name='leave_circle'),
    path('my-circles/', views.my_circles, name='my_circles'),
    path('post/create/<int:circle_id>/', views.create_post, name='create_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
]
