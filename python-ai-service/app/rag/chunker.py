from types import SimpleNamespace

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    RecursiveCharacterTextSplitter = None


def split_documents(documents):
    """
    Split documents into smaller chunks.
    """
    if RecursiveCharacterTextSplitter is not None:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        return text_splitter.split_documents(documents)

    chunks = []
    for doc in documents:
        text = getattr(doc, "page_content", str(doc))
        metadata = getattr(doc, "metadata", {})
        step = 450
        for i in range(0, max(len(text), 1), step):
            chunk_text = text[i:i + 500]
            if chunk_text:
                chunks.append(SimpleNamespace(page_content=chunk_text, metadata=dict(metadata)))
    return chunks