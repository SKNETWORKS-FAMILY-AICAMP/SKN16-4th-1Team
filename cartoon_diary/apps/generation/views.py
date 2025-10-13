"""API surface for generation pipeline control."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.diaries.models import DiaryEntry

from .pipelines import trigger_cartoon_generation
from .selectors import get_latest_cartoon_for_entry
from .services import enqueue_generation


class CartoonGenerateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, diary_entry_id: int, *args, **kwargs):
        diary_entry = get_object_or_404(DiaryEntry, pk=diary_entry_id, user=request.user)
        cartoon = enqueue_generation(diary_entry=diary_entry)
        trigger_cartoon_generation(diary_entry_id=diary_entry.id)
        return Response({"cartoon_id": cartoon.id, "status": cartoon.status}, status=status.HTTP_202_ACCEPTED)


class CartoonStatusView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, diary_entry_id: int, *args, **kwargs):
        cartoon = get_latest_cartoon_for_entry(diary_entry_id=diary_entry_id)
        if not cartoon:
            return Response({"detail": "No cartoon found"}, status=status.HTTP_404_NOT_FOUND)
        panels = [
            {
                "index": panel.index,
                "image": panel.image.url if panel.image else None,
                "caption": panel.caption,
            }
            for panel in cartoon.panels.all()
        ]
        return Response(
            {
                "cartoon_id": cartoon.id,
                "status": cartoon.status,
                "grid_image": cartoon.grid_image.url if cartoon.grid_image else None,
                "panels": panels,
            }
        )
