"""Models for the resume app."""

from django.db import models

from resume.validators import validate_pdf_file


class Resume(models.Model):
    """Singleton record holding the owner's resume content and PDF."""

    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    file = models.FileField(upload_to="resume/", validators=[validate_pdf_file])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return a fixed label since only one resume record should exist."""
        return "Resume"

    def save(self, *args, **kwargs) -> None:
        """Force a single primary key so only one resume record ever exists."""
        self.pk = 1
        super().save(*args, **kwargs)
