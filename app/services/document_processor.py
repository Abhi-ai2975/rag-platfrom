# import uuid
# import hashlib

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk
from app.models.document import Document

from app.services.cleaner import clean_text
from app.services.chunker import chunk_text
from app.services.extractor import extract_text



# def calculate_file_hash(content: bytes) -> str:
#     return hashlib.sha256(content).hexdigest()


# def generate_storage_name(extension: str) -> str:
#     return f"{uuid.uuid4()}{extension}"


def process_document(
    document: Document,
    db: Session,
) -> None:

    document.status = "processing"
    db.commit()

    try:
        extracted_sections = extract_text(
            document.file_path
        )

        all_chunks = []

        for section in extracted_sections:

            cleaned = clean_text(
                section["text"]
            )

            if not cleaned:
                continue

            chunks = chunk_text(
                cleaned
            )

            for chunk in chunks:
                all_chunks.append({
                    "content": chunk,
                    "metadata": {
                        "source": document.filename,
                        "section": section,
                    },
                })

        if not all_chunks:
            raise ValueError(
                "No extractable text found in document."
            )

        for index, item in enumerate(all_chunks):

            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=item["content"],
                metadata_json=str(
                    item["metadata"]
                ),
            )

            db.add(db_chunk)

        document.char_count = sum(
            len(item["content"])
            for item in all_chunks
        )

        document.status = "completed"
        document.processed_at = datetime.utcnow()
        document.error_message = None

        db.commit()

    except Exception as exc:

        document.status = "failed"
        document.error_message = str(exc)

        db.commit()

        raise
