"""Public views for the research archive."""

from django.views.generic import ListView

from research.models import Research


class ResearchListView(ListView):
    """List published research entries newest first."""

    model = Research
    template_name = "research/research_list.html"
    context_object_name = "research_entries"

    def get_queryset(self):
        """Return only published research in reverse publication order."""
        return Research.objects.filter(is_published=True).order_by(
            "-publication_date", "title"
        )
