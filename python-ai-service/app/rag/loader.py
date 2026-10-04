from pathlib import Path
from types import SimpleNamespace

try:
    from langchain_community.document_loaders import PyPDFLoader
except ImportError:
    PyPDFLoader = None


def load_pdf(file_path):
    """
    Load a PDF file and return its documents.
    """
    if PyPDFLoader is not None:
        loader = PyPDFLoader(file_path)
        return loader.load()

    raw_bytes = Path(file_path).read_bytes()
    text = raw_bytes.decode("latin-1", errors="ignore")
    return [SimpleNamespace(page_content=text, metadata={"source": str(file_path)})]