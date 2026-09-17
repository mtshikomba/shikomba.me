"""URL routes for the research archive."""

from django.urls import path

from research import views

app_name = "research"

urlpatterns = [
    path("", views.ResearchListView.as_view(), name="research-list"),
]
