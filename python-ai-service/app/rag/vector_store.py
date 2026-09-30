from langchain_chroma import Chroma


def create_vector_store(chunks, embeddings, persist_directory="./chroma_db"):
    """
    Store document chunks and their embeddings in ChromaDB.
    """

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return vectorstore