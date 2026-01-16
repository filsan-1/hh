from django.contrib import admin
from .models import HormonalTwin, TwinConnection

@admin.register(HormonalTwin)
class HormonalTwinAdmin(admin.ModelAdmin):
    list_display = ('user', 'primary_issue', 'created_at')
    list_filter = ('primary_issue', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TwinConnection)
class TwinConnectionAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user1__username', 'user2__username')
