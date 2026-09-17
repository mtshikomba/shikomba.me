"""Django admin registration for the projects app."""

from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin authoring interface for projects."""

    list_display = ("title", "status", "is_open_source", "is_published")
    list_filter = ("status", "is_open_source", "is_published")
    search_fields = ("title", "short_description", "tags")
