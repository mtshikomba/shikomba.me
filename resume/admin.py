"""Django admin registration for the resume app."""

from django.contrib import admin

from resume.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """Admin authoring interface for the single resume record."""

    list_display = ("__str__", "updated_at")

    def has_add_permission(self, request) -> bool:
        """Disallow adding more than one resume record."""
        return not Resume.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        """Disallow deleting the resume record."""
        return False
