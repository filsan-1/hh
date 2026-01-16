from django.db import models
from django.contrib.auth.models import User

class SupportCircle(models.Model):
    """Model for support circles - groups of women supporting each other"""
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_circles')
    members = models.ManyToManyField(User, related_name='support_circles')
    focus_area = models.CharField(
        max_length=100,
        choices=[
            ('PCOS', 'PCOS Support'),
            ('Endometriosis', 'Endometriosis Support'),
            ('Thyroid', 'Thyroid Disorders'),
            ('Mental_Health', 'Mental Health & Hormones'),
            ('Nutrition', 'Nutrition & Wellness'),
            ('Fitness', 'Fitness & Exercise'),
            ('Fertility', 'Fertility Journey'),
            ('General', 'General Hormonal Health'),
        ]
    )
    icon = models.CharField(max_length=50, default='👥')
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class CirclePost(models.Model):
    """Model for posts within a support circle"""
    circle = models.ForeignKey(SupportCircle, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.circle.name}"


class CircleComment(models.Model):
    """Model for comments on circle posts"""
    post = models.ForeignKey(CirclePost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class CircleLike(models.Model):
    """Model for likes on circle posts"""
    post = models.ForeignKey(CirclePost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
