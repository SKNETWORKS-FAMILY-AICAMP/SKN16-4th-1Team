"""Template views for diary pages."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "diaries/calendar.html"
