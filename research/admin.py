"""Django admin registration for the research archive."""

from django.contrib import admin

from research.models import Research


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    """Admin authoring interface for research entries."""

    list_display = ("title", "publication_date", "is_published")
    list_filter = ("is_published", "publication_date")
    search_fields = ("title", "summary")
    date_hierarchy = "publication_date"
