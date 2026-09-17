"""Views for the resume app: on-site rendering and PDF download."""

from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from resume.models import Resume


def resume_detail(request: HttpRequest) -> HttpResponse:
    """Render the resume content on-site, if configured."""
    resume = Resume.objects.first()
    return render(request, "resume/resume_detail.html", {"resume": resume})


def resume_download(request: HttpRequest) -> FileResponse:
    """Stream the stored resume PDF as a file download."""
    resume = Resume.objects.first()
    if not resume or not resume.file:
        raise Http404("No resume file is available.")

    return FileResponse(
        resume.file.open("rb"),
        as_attachment=True,
        filename="resume.pdf",
        content_type="application/pdf",
    )
