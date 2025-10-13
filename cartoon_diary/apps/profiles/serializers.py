"""Serializers for profile operations."""

from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "nickname", "avatar", "timezone")
