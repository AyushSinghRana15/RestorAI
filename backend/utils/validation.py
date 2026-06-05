from pathlib import Path

from fastapi import UploadFile

from backend.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


def validate_image(file: UploadFile) -> None:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")
    content = file.file.read()
    file.file.seek(0)
    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File exceeds maximum size of 20 MB")
