def retrieve_documents(vectorstore, query, k=3):
    """
    Retrieve the most relevant documents for a user query.
    """

    results = vectorstore.similarity_search(query, k=k)

    return results