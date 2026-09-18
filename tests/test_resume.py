"""Tests for the resume app: rendering, download, and upload validation."""

import io

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from resume.models import Resume
from resume.validators import validate_pdf_file

PDF_CONTENT = b"%PDF-1.4\n%mock pdf content\n"


class ResumeDetailViewTests(TestCase):
    """Tests for the on-site resume page."""

    def test_resume_page_renders_without_resume(self):
        response = self.client.get(reverse("resume:resume-detail"))

        self.assertEqual(response.status_code, 200)

    def test_resume_intro_uses_shared_page_intro_structure(self):
        response = self.client.get(reverse("resume:resume-detail"))

        self.assertContains(response, 'class="page-intro"')
        self.assertNotContains(response, "page-intro--split")

    def test_resume_page_renders_content(self):
        Resume.objects.create(
            experience="Worked on things.",
            education="Studied things.",
            skills="Python, Django",
            file=SimpleUploadedFile(
                "resume.pdf", PDF_CONTENT, content_type="application/pdf"
            ),
        )

        response = self.client.get(reverse("resume:resume-detail"))

        self.assertContains(response, "Worked on things.")
        self.assertContains(response, "Python, Django")

    def test_resume_download_uses_dedicated_spacing_wrapper(self):
        Resume.objects.create(
            file=SimpleUploadedFile(
                "resume.pdf", PDF_CONTENT, content_type="application/pdf"
            ),
        )

        response = self.client.get(reverse("resume:resume-detail"))

        self.assertContains(response, 'class="resume-download"')
        self.assertContains(response, 'href="/resume/download/"')


class ResumeDownloadViewTests(TestCase):
    """Tests for the resume PDF download route."""

    def test_download_returns_pdf(self):
        Resume.objects.create(
            file=SimpleUploadedFile(
                "resume.pdf", PDF_CONTENT, content_type="application/pdf"
            ),
        )

        response = self.client.get(reverse("resume:resume-download"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_download_404s_without_a_resume(self):
        response = self.client.get(reverse("resume:resume-download"))

        self.assertEqual(response.status_code, 404)


class ResumeUploadValidationTests(TestCase):
    """Tests for the resume PDF upload validator."""

    def test_rejects_non_pdf_extension(self):
        upload = SimpleUploadedFile(
            "resume.txt", PDF_CONTENT, content_type="text/plain"
        )

        with self.assertRaises(ValidationError):
            validate_pdf_file(upload)

    def test_rejects_file_without_pdf_signature(self):
        upload = SimpleUploadedFile(
            "resume.pdf", b"not a real pdf", content_type="application/pdf"
        )

        with self.assertRaises(ValidationError):
            validate_pdf_file(upload)

    def test_rejects_oversized_file(self):
        oversized_content = io.BytesIO(PDF_CONTENT + b"0" * (5 * 1024 * 1024 + 1))
        upload = SimpleUploadedFile(
            "resume.pdf", oversized_content.read(), content_type="application/pdf"
        )

        with self.assertRaises(ValidationError):
            validate_pdf_file(upload)

    def test_accepts_valid_pdf(self):
        upload = SimpleUploadedFile(
            "resume.pdf", PDF_CONTENT, content_type="application/pdf"
        )

        validate_pdf_file(upload)
