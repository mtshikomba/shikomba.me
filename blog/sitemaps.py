"""Sitemap configuration for the blog app."""

from django.contrib.sitemaps import Sitemap

from blog.models import Post


class PostSitemap(Sitemap):
    """Sitemap entries for published posts only."""

    changefreq = "weekly"
    priority = 0.6

    def items(self):
        """Return the published posts to include in the sitemap."""
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def lastmod(self, obj: Post):
        """Return the last-modified timestamp for a post."""
        return obj.updated_at
