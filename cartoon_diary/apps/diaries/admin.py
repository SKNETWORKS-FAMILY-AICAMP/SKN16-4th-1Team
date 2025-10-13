"""Diary admin configuration."""

from django.contrib import admin

from .models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "mood", "created_at")
    list_filter = ("mood", "date")
    search_fields = ("user__email", "content")
