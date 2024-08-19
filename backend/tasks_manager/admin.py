from django.contrib import admin
from .models import UserMessage, Task


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_message')
    search_fields = ('user__username', 'original_message')
    list_filter = ('user',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'start_time', 'notification_time', 'create_at')
    search_fields = ('user__username', 'name', 'description')
    list_filter = ('user', 'start_time', 'create_at')
    date_hierarchy = 'start_time'
