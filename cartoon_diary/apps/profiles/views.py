"""Profile API views."""

from rest_framework import generics, permissions

from .selectors import get_profile_for_user
from .serializers import ProfileSerializer


class MeProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_profile_for_user(user=self.request.user)
