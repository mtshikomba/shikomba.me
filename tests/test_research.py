"""Tests for the published research archive."""

from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from research.models import Research


def make_research(**overrides) -> Research:
    """Create a Research entry with sensible defaults."""
    defaults = {
        "title": "Published Research",
        "summary": "A concise research summary.",
        "publication_date": date.today() - timedelta(days=1),
        "url": "https://example.com/research",
        "is_published": True,
    }
    defaults.update(overrides)
    return Research.objects.create(**defaults)


class ResearchListViewTests(TestCase):
    """Tests for the public research list."""

    def test_only_published_research_is_listed(self):
        make_research(title="Published Work")
        make_research(title="Draft Work", is_published=False)

        response = self.client.get(reverse("research:research-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Work")
        self.assertNotContains(response, "Draft Work")

    def test_research_is_ordered_newest_first(self):
        make_research(
            title="Older Work",
            publication_date=date.today() - timedelta(days=10),
        )
        make_research(
            title="Newer Work",
            publication_date=date.today() - timedelta(days=2),
            url="https://example.com/newer",
        )

        response = self.client.get(reverse("research:research-list"))

        self.assertLess(
            response.content.index(b"Newer Work"),
            response.content.index(b"Older Work"),
        )

    def test_entry_renders_metadata_summary_and_link(self):
        research = make_research()

        response = self.client.get(reverse("research:research-list"))

        self.assertContains(response, research.title)
        self.assertContains(response, research.summary)
        self.assertContains(response, research.publication_date.strftime("%B"))
        self.assertContains(response, 'href="https://example.com/research"')
        self.assertContains(response, "Read publication")

    def test_research_route_is_successful_with_no_entries(self):
        response = self.client.get(reverse("research:research-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No published research yet.")

    def test_navigation_marks_research_as_current(self):
        response = self.client.get(reverse("research:research-list"))

        self.assertContains(
            response,
            '<a href="/research/" aria-current="page">Research</a>',
        )
