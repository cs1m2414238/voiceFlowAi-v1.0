def parse_response(response):
    """
    Extract the text content from the LLM response.
    """

    return response.content.strip()