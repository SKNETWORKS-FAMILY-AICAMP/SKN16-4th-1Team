"""Diary API serializers."""

from rest_framework import serializers

from ..models import DiaryEntry


class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = (
            "id",
            "date",
            "title",
            "content",
            "mood",
            "tags",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
