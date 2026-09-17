"""Validators for the resume app."""

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024
PDF_MAGIC_BYTES = b"%PDF-"


def validate_pdf_file(value: UploadedFile) -> None:
    """Reject uploads that are not a small, genuine PDF file.

    Checks the extension, a magic-byte signature, and the file size, since a
    permissive ``FileField`` would otherwise allow an unrestricted file upload.
    """
    name = value.name or ""
    if not name.lower().endswith(".pdf"):
        raise ValidationError("Resume file must have a .pdf extension.")

    if value.size > MAX_RESUME_SIZE_BYTES:
        raise ValidationError("Resume file must be smaller than 5MB.")

    position = value.file.tell()
    try:
        value.file.seek(0)
        header = value.file.read(len(PDF_MAGIC_BYTES))
    finally:
        value.file.seek(position)

    if header != PDF_MAGIC_BYTES:
        raise ValidationError("Resume file does not look like a valid PDF.")
