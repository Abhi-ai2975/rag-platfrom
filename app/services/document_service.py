from pathlib import Path
import uuid
import hashlib

def generate_storage_name(extension: str) -> str:
    return f"{uuid.uuid4()}{extension}"

def calculate_file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

def validate_file(filename: str, file_size: int) -> None:
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupport file type: {extension}"
        )

    if file_size > MAX_FILE_SIZE:
	    raise ValueError(
	        f"File size exceeds 20 MB limit"
	    )



