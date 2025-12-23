from django.contrib import admin

from .models import Run, Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    pass
