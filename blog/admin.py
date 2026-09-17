"""Django admin registration for the blog app."""

from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin authoring interface for blog posts."""

    list_display = ("title", "status", "publish_date", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_date"
