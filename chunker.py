def create_chunks(pages, chunk_size=500, overlap=100):
    """
    Split document text into overlapping chunks.

    Each chunk keeps its original page number
    so we can later show exact citations.
    """

    chunks = []

    for page in pages:
        text = page["text"].strip()
        page_number = page["page"]

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "page": page_number
            })

            if end >= len(text):
                break

            start = end - overlap

    return chunks