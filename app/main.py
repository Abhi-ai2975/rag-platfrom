from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.qdrant import qdrant_client
from app.api.routes.documents import router as document_router


app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
)

app.include_router(
    document_router,
    prefix="/api/v1",
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


@app.get("/health/database")
def database_health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    value = result.scalar()

    return {
        "database": "connected",
        "test": value,
    }


@app.get("/health/qdrant")
def qdrant_health():
    collections = qdrant_client.get_collections()

    return {
	"qdrant": "connected",
	"collections": [
	    collection.name
	    for collection in collections.collections
	],
    }
