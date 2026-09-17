"""Views for the blog app: post list/detail and the about page."""

from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

from blog.models import Post


class PostListView(ListView):
    """Paginated list of published posts."""

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        """Return only published posts, most recent first."""
        return Post.objects.filter(
            status=Post.Status.PUBLISHED, publish_date__lte=timezone.now()
        ).order_by("-publish_date")


class PostDetailView(DetailView):
    """Detail view for a single published post."""

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        """Restrict lookups to published posts so drafts 404."""
        return Post.objects.filter(
            status=Post.Status.PUBLISHED, publish_date__lte=timezone.now()
        )


class AboutView(TemplateView):
    """Static about/bio page."""

    template_name = "blog/about.html"


def robots_txt(request: HttpRequest) -> HttpResponse:
    """Serve a robots.txt that allows crawling and points to the sitemap."""
    lines = [
        "User-Agent: *",
        "Allow: /",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
