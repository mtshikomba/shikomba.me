"""Views for the projects app."""

from django.views.generic import ListView

from projects.models import Project


class ProjectListView(ListView):
    """List of published projects, ongoing and past."""

    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        """Return only published projects."""
        return Project.objects.filter(is_published=True)
