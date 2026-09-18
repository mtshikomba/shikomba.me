"""Models for the research archive."""

from django.db import models


class Research(models.Model):
    """A published or draft research work."""

    title = models.CharField(max_length=200)
    summary = models.TextField()
    publication_date = models.DateField()
    url = models.URLField()
    is_published = models.BooleanField(default=False)

    class Meta:
        """Model metadata."""

        ordering = ["-publication_date", "title"]

    def __str__(self) -> str:
        """Return the research title for display."""
        return self.title
