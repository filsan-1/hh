from django.urls import path
from . import views

app_name = 'Spousal_Education'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('categories/', views.category_list, name='category_list'),
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('article/<slug:slug>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
