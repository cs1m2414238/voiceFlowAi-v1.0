def create_rag_prompt(context, question):
    """
    Create a prompt that instructs the LLM
    to answer using only the retrieved context.
    """

    prompt = f"""
You are a customer support assistant.

Answer the user's question using ONLY the information
provided in the context.

If the answer is not present in the context,
say: "I don't have that information in the knowledge base."

Context:
{context}

User Question:
{question}

Answer:
"""

    return prompt