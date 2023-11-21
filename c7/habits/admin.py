from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class MailSettingsAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'time', 'is_public', 'is_pleasant')
    list_filter = ('user',)
    search_fields = ('is_pleasant',)
