"""Diary API views."""

from rest_framework import mixins, viewsets

from ..models import DiaryEntry
from ..services import save_diary_entry
from .serializers import DiaryEntrySerializer


class DiaryEntryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = DiaryEntrySerializer

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user).order_by("-date")


class DiaryEntryWriteViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = DiaryEntrySerializer

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        entry = save_diary_entry(
            user=self.request.user,
            entry_date=serializer.validated_data["date"],
            content=serializer.validated_data["content"],
            title=serializer.validated_data.get("title"),
            mood=serializer.validated_data.get("mood"),
            tags=serializer.validated_data.get("tags"),
        )
        serializer.instance = entry

    def perform_update(self, serializer):
        instance = serializer.instance
        entry = save_diary_entry(
            user=self.request.user,
            entry_date=instance.date,
            content=serializer.validated_data.get("content", instance.content),
            title=serializer.validated_data.get("title", instance.title),
            mood=serializer.validated_data.get("mood", instance.mood),
            tags=serializer.validated_data.get("tags", instance.tags),
        )
        serializer.instance = entry
