from django.contrib import admin
from .models import SupportCircle, CirclePost, CircleComment, CircleLike

@admin.register(SupportCircle)
class SupportCircleAdmin(admin.ModelAdmin):
    list_display = ('name', 'focus_area', 'creator', 'created_at')
    list_filter = ('focus_area', 'is_private', 'created_at')
    search_fields = ('name', 'description', 'creator__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CirclePost)
class CirclePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'circle', 'author', 'created_at')
    list_filter = ('circle', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CircleComment)
class CircleCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CircleLike)
class CircleLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')
