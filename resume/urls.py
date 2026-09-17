"""URL routes for the resume app."""

from django.urls import path

from resume import views

app_name = "resume"

urlpatterns = [
    path("", views.resume_detail, name="resume-detail"),
    path("download/", views.resume_download, name="resume-download"),
]
