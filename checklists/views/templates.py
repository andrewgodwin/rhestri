from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..models import Run, Template


class ListTemplates(LoginRequiredMixin, ListView):

    template_name = "checklist_templates/list.html"
    context_object_name = "templates"
    extra_context = {"section": "checklist_templates"}

    def get_queryset(self) -> QuerySet[Template]:
        return Template.objects.filter(user=self.request.user)
