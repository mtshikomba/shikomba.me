"""App configuration for the research archive."""

from django.apps import AppConfig


class ResearchConfig(AppConfig):
    """Configuration for the research app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "research"
