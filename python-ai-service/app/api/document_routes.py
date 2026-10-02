
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.rag.parser import ingest_pdf


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

CHROMA_DIR = Path(__file__).resolve().parents[2] / "chroma_test_db"


@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    temporary_path = None

    try:
        with NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temp_file:
            temporary_path = Path(temp_file.name)
            content = file.file.read()
            temp_file.write(content)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty."
            )

        chunk_count, _ = ingest_pdf(
            file_path=str(temporary_path),
            persist_directory=str(CHROMA_DIR)
        )

        return {
            "message": "Document processed successfully.",
            "filename": file.filename,
            "chunks_created": chunk_count
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {exc}"
        ) from exc
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()
        file.file.close()