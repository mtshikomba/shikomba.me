"""Models for the projects app."""

from django.db import models


class Project(models.Model):
    """A past or ongoing project shown in the public showcase."""

    class Status(models.TextChoices):
        """Whether a project is still active or finished."""

        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"

    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=280)
    role = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices)
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated technology tags, e.g. 'Django, PostgreSQL'.",
    )
    source_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    is_open_source = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        """Model metadata."""

        ordering = ["-start_date", "title"]

    def __str__(self) -> str:
        """Return the project title for display."""
        return self.title

    def tag_list(self) -> list[str]:
        """Return the tags as a clean list of strings."""
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
