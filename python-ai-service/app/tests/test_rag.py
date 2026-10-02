
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rag_endpoint_returns_answer():
    response = client.post(
        "/rag/ask",
        json={"question": "How long does a refund take?"}
    )

    assert response.status_code == 200
    assert "answer" in response.json()
    assert len(response.json()["answer"]) > 0
    
    

def test_document_upload_rejects_non_pdf():
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "notes.txt",
                b"This is not a PDF",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please upload a PDF file."