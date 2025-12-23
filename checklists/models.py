import urlman
import pydantic
from django_pydantic_field import SchemaField

from django.db import models
from django.utils.functional import cached_property


class ChecklistItem(pydantic.BaseModel):
    """
    An item in a checklist.

    Used in both the template and the run.
    """

    name: str
    description: str = ""

    heading: bool = False
    complete: bool = False
    skipped: bool = False

    conditions: list[str] = []
    external_ids: list[str] = []


class Template(models.Model):
    """
    An overall template for a checklist. It's instantiated into Runs.
    """

    name = models.CharField(max_length=255, unique=True)

    items: list[ChecklistItem] = SchemaField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class urls(urlman.Urls):
        list = "/checklists/templates/"
        view = "{list}{self.id}/"
        edit = "{view}edit/"
        delete = "{view}delete/"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.urls.view

    @cached_property
    def conditions(self):
        """
        Returns a list of conditionals that this checklist needs to be run
        """
        result = set()
        for item in self.items:
            result.update(item.conditions)
        return sorted(result)


class Run(models.Model):
    """
    A usage/instance of a checklist.

    Copies over the items from the main template so that future edits to it
    do not mysteriously propagate to this one.
    """

    template = models.ForeignKey(
        "checklists.Template", on_delete=models.CASCADE, related_name="runs"
    )
    name = models.CharField(max_length=255, unique=True)
    conditions: list[str] = SchemaField()

    items: list[ChecklistItem] = SchemaField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class urls(urlman.Urls):
        list = "/checklists/runs/"
        view = "{list}{self.id}/"
        post_create = "{view}post-create/"
        edit = "{view}edit/"
        delete = "{view}delete/"
        setup_scan = "{view}setup-scan/"
        stop_scan = "{view}stop-scan/"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.urls.view
