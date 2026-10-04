from langchain_ollama import ChatOllama


def get_llm():
    """
    Create and return the local Llama 3.2 model.
    """

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )

    return llm