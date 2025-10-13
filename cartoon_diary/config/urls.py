"""Root URL configuration for the cartoon diary project."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/profile/", include("apps.profiles.urls")),
    path("api/diaries/", include("apps.diaries.api.urls")),
    path("api/cartoons/", include("apps.generation.urls")),
]
