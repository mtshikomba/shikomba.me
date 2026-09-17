"""URL routes for the blog app."""

from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
]
