from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document import Document
from app.services.document_service import (
    MAX_FILE_SIZE,
    calculate_file_hash,
    validate_file,
)
from app.services.document_processor import process_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

STORAGE_DIR = Path("data/documents")
STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post("/upload")
async def upload_document(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    content = await file.read()

    try:
        validate_file(
            filename=file.filename,
            file_size=len(content),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    file_hash = calculate_file_hash(content)

    existing_document = (
        db.query(Document)
        .filter(
            Document.user_id == user_id,
            Document.file_hash == file_hash,
        )
        .first()
    )

    if existing_document:
        raise HTTPException(
            status_code=409,
            detail="This document has already been uploaded.",
        )

    extension = Path(file.filename).suffix.lower()

    storage_name = (
        f"{uuid4()}{extension}"
    )

    storage_path = STORAGE_DIR / storage_name

    storage_path.write_bytes(content)

    document = Document(
        user_id=user_id,
        filename=file.filename,
        file_path=str(storage_path),
        file_type=extension,
        file_size=len(content),
        file_hash=file_hash,
        status="uploaded",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    process_document(
        document=document,
        db=db,
    )

    return {
        "id": document.id,
        "filename": document.filename,
        "status": document.status,
    }
