"""Tests for the projects app: visibility, open-source marking, and links."""

from django.test import TestCase
from django.urls import reverse

from projects.models import Project


def make_project(**overrides) -> Project:
    """Create a Project with sensible defaults, overridable per test."""
    defaults = {
        "title": "Test Project",
        "short_description": "A test project.",
        "status": Project.Status.ONGOING,
        "is_published": True,
    }
    defaults.update(overrides)
    return Project.objects.create(**defaults)


class ProjectListViewTests(TestCase):
    """Tests for the public project list view."""

    def test_only_published_projects_are_listed(self):
        make_project(title="Published")
        make_project(title="Unpublished", is_published=False)

        response = self.client.get(reverse("projects:project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published")
        self.assertNotContains(response, "Unpublished")

    def test_open_source_project_shows_source_link(self):
        make_project(
            title="Open Project",
            is_open_source=True,
            source_url="https://example.com/repo",
        )

        response = self.client.get(reverse("projects:project-list"))

        self.assertContains(response, "https://example.com/repo")

    def test_non_open_source_project_hides_source_link(self):
        make_project(
            title="Closed Project",
            is_open_source=False,
            source_url="https://example.com/should-not-appear",
        )

        response = self.client.get(reverse("projects:project-list"))

        self.assertNotContains(response, "https://example.com/should-not-appear")

    def test_project_without_demo_url_shows_no_demo_link(self):
        make_project(title="No Demo Project", demo_url="")

        response = self.client.get(reverse("projects:project-list"))

        self.assertContains(response, "No Demo Project")
        self.assertNotContains(response, "Live demo")
