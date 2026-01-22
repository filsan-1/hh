from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class ArticleCategory(models.Model):
    """Categories for educational articles"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='📚', help_text='Emoji or icon for the category')
    color = models.CharField(max_length=7, default='#FF69B4', help_text='Hex color code')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Article Categories'
    
    def __str__(self):
        return self.name
    
    def get_article_count(self):
        return self.articles.filter(is_published=True).count()


class EducationalArticle(models.Model):
    """Educational articles for spouses about women's health"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='educational_articles')
    
    # Content
    summary = models.TextField(max_length=500, help_text='Brief summary of the article')
    content = models.TextField(help_text='Main content of the article')
    key_takeaways = models.TextField(blank=True, help_text='Bullet points of key takeaways')
    
    # Metadata
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    estimated_read_time = models.IntegerField(default=5, help_text='Estimated reading time in minutes')
    is_published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, help_text='Display on featured section')
    
    # Engagement
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Educational Article'
        verbose_name_plural = 'Educational Articles'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('Spousal_Education:article_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ArticleLike(models.Model):
    """Track likes for articles"""
    article = models.ForeignKey(EducationalArticle, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('article', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"


class ArticleBookmark(models.Model):
    """Bookmarks/saved articles for users"""
    article = models.ForeignKey(EducationalArticle, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('article', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.article.title}"


class ArticleComment(models.Model):
    """Comments on educational articles"""
    article = models.ForeignKey(EducationalArticle, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"
