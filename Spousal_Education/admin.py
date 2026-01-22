from django.contrib import admin
from .models import ArticleCategory, EducationalArticle, ArticleLike, ArticleBookmark, ArticleComment


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'get_article_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('created_at',)


@admin.register(EducationalArticle)
class EducationalArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'difficulty_level', 'is_published', 'featured', 'views_count', 'likes_count', 'published_date')
    list_filter = ('is_published', 'featured', 'difficulty_level', 'category', 'published_date')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at')
    list_editable = ('is_published', 'featured')
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Content', {
            'fields': ('summary', 'content', 'key_takeaways')
        }),
        ('Metadata', {
            'fields': ('difficulty_level', 'estimated_read_time', 'is_published', 'featured')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('published_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'article__title')
    readonly_fields = ('created_at',)


@admin.register(ArticleBookmark)
class ArticleBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'article__title')
    readonly_fields = ('created_at',)


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'article__title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_approved',)
