"""Admin registrations for generation models."""

from django.contrib import admin

from .models import Cartoon, CartoonPanel, Prompt


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("id", "diary_entry", "model", "created_at")


@admin.register(Cartoon)
class CartoonAdmin(admin.ModelAdmin):
    list_display = ("id", "diary_entry", "status", "version", "created_at")
    list_filter = ("status",)


@admin.register(CartoonPanel)
class CartoonPanelAdmin(admin.ModelAdmin):
    list_display = ("id", "cartoon", "index")
