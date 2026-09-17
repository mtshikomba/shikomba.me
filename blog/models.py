"""Models for the blog app."""

from django.db import models
from django.urls import reverse


class Post(models.Model):
    """A single blog post."""

    class Status(models.TextChoices):
        """Publication status for a post."""

        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    publish_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata."""

        ordering = ["-publish_date"]

    def __str__(self) -> str:
        """Return the post title for display."""
        return self.title

    def get_absolute_url(self) -> str:
        """Return the canonical detail URL for this post."""
        return reverse("blog:post-detail", kwargs={"slug": self.slug})
