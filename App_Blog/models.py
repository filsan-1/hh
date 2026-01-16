from django.db import models
from django.contrib.auth.models import User
from django.db.models import fields

# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='post_author')
    blog_title = models.CharField(max_length=264, verbose_name="Put a Title")
    slug = models.SlugField(max_length=264, unique=True)
    blog_content = models.TextField(verbose_name="What is on your mind?")
    blog_image = models.ImageField(upload_to='blog_images', verbose_name="Blog Image")
    public_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['-public_date']
   


    def __str__(self):
        return self.blog_title

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_comment')
    comment =models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering =['-comment_date']
   


    def __str__(self):
        return self.comment

class Likes(models.Model):
    blog =models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='liked_blog')
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='liked_user')


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_author')
    recipe_title = models.CharField(max_length=264, verbose_name="Recipe Title")
    slug = models.SlugField(max_length=264, unique=True)
    description = models.TextField(verbose_name="Recipe Description", blank=True)
    ingredients = models.TextField(verbose_name="Ingredients (one per line)")
    instructions = models.TextField(verbose_name="Cooking Instructions")
    servings = models.IntegerField(default=4)
    prep_time = models.IntegerField(help_text="Prep time in minutes", default=15)
    cook_time = models.IntegerField(help_text="Cook time in minutes", default=30)
    recipe_image = models.ImageField(upload_to='recipe_images', verbose_name="Recipe Image")
    public_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-public_date']

    def __str__(self):
        return self.recipe_title


    


