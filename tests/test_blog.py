"""Tests for the blog app: post visibility, routing, about page, and SEO plumbing."""

from datetime import timedelta
from pathlib import Path

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Post


def make_post(**overrides) -> Post:
    """Create a Post with sensible defaults, overridable per test."""
    defaults = {
        "title": "Test Post",
        "slug": "test-post",
        "body": "Body content.",
        "status": Post.Status.PUBLISHED,
        "publish_date": timezone.now() - timedelta(days=1),
    }
    defaults.update(overrides)
    return Post.objects.create(**defaults)


class PostListViewTests(TestCase):
    """Tests for the public post list view."""

    def test_blog_stylesheet_has_no_decorative_hero_circle(self):
        stylesheet = (
            Path(__file__).resolve().parents[1] / "static" / "css" / "site.css"
        ).read_text()

        self.assertIn(".hero {", stylesheet)
        self.assertIn(".hero__lede", stylesheet)
        self.assertIn("font-size: 1.1rem;", stylesheet)
        self.assertNotIn(".hero::after", stylesheet)

    def test_only_published_posts_are_listed(self):
        make_post(title="Published", slug="published", status=Post.Status.PUBLISHED)
        make_post(title="Draft", slug="draft", status=Post.Status.DRAFT)

        response = self.client.get(reverse("blog:post-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published")
        self.assertNotContains(response, "Draft")

    def test_future_published_post_is_not_listed(self):
        make_post(
            title="Future Post",
            slug="future-post",
            status=Post.Status.PUBLISHED,
            publish_date=timezone.now() + timedelta(days=1),
        )

        response = self.client.get(reverse("blog:post-list"))

        self.assertNotContains(response, "Future Post")


class PostDetailViewTests(TestCase):
    """Tests for the public post detail view."""

    def test_published_post_detail_renders(self):
        post = make_post()

        response = self.client.get(
            reverse("blog:post-detail", kwargs={"slug": post.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)

    def test_draft_post_returns_404(self):
        post = make_post(status=Post.Status.DRAFT)

        response = self.client.get(
            reverse("blog:post-detail", kwargs={"slug": post.slug})
        )

        self.assertEqual(response.status_code, 404)

    def test_unknown_slug_returns_404(self):
        response = self.client.get(
            reverse("blog:post-detail", kwargs={"slug": "does-not-exist"})
        )

        self.assertEqual(response.status_code, 404)


class AboutViewTests(TestCase):
    """Tests for the about page."""

    def test_about_page_renders(self):
        response = self.client.get(reverse("blog:about"))

        self.assertEqual(response.status_code, 200)

    def test_about_page_renders_contact_links(self):
        response = self.client.get(reverse("blog:about"))

        self.assertContains(response, 'href="mailto:tangenishikomba@gmail.com"')
        self.assertContains(response, "Email Matheus T. Shikomba")
        self.assertContains(
            response, 'href="https://www.linkedin.com/in/tangeni-shikomba"'
        )
        self.assertContains(response, "LinkedIn profile")
        self.assertContains(response, 'href="https://github.com/mtshikomba"')
        self.assertContains(response, "GitHub profile")

    def test_about_page_renders_profile_image(self):
        response = self.client.get(reverse("blog:about"))

        self.assertContains(response, "/static/images/tangeni-shikomba-profile.jpg")
        self.assertContains(response, 'alt="Portrait of Matheus T. Shikomba"')

    def test_public_shell_renders_brand_image_and_footer_links(self):
        response = self.client.get(reverse("blog:about"))

        self.assertContains(response, "/static/images/tangeni-shikomba-brand.jpg")
        self.assertEqual(
            response.content.count(b"tangeni-shikomba-brand.jpg"),
            1,
        )
        self.assertContains(response, 'alt=""')
        self.assertContains(response, "Matheus T. Shikomba")
        self.assertContains(response, 'class="site-footer__copy"')
        self.assertContains(response, 'class="site-footer__links"')
        self.assertContains(response, 'href="https://github.com/mtshikomba"')
        self.assertContains(response, 'href="mailto:tangenishikomba@gmail.com"')
        self.assertContains(
            response, 'href="https://www.linkedin.com/in/tangeni-shikomba"'
        )
        self.assertNotContains(response, ">shikomba<span")


class SeoPlumbingTests(TestCase):
    """Tests for robots.txt and the XML sitemap."""

    def test_robots_txt_responds_successfully(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sitemap:", response.content)

    def test_sitemap_lists_only_published_posts(self):
        make_post(title="Published", slug="published", status=Post.Status.PUBLISHED)
        make_post(title="Draft", slug="draft", status=Post.Status.DRAFT)

        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/published/")
        self.assertNotContains(response, "/draft/")
