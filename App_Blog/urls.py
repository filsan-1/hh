from django.urls import path
from . import views

app_name='App_Blog'


urlpatterns = [
    path('',views.BlogList.as_view(),name='blog_list'),
    path('write/',views.CreateBlog.as_view(),name='create_blog'),
    path('details/<slug:slug>',views.blog_details,name='blog_details'),
    path('liked/<pk>/',views.liked,name='liked_post'),
    path('unliked/<pk>/',views.unliked,name='unliked_post'),
    path('my-blog/',views.MyBlogs.as_view(),name='my_blogs'),
    path('edit-blog/<pk>/',views.UpdateBlog.as_view(),name='edit_blog'),
    
    # Recipe URLs
    path('recipes/', views.RecipeList.as_view(), name='recipe_list'),
    path('recipes/<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('recipes/add/', views.CreateRecipe.as_view(), name='create_recipe'),
    path('recipes/edit/<pk>/', views.UpdateRecipe.as_view(), name='edit_recipe'),
    path('recipes/delete/<pk>/', views.DeleteRecipe.as_view(), name='delete_recipe'),
]
