import fitz  # PyMuPDF

def load_pdf_chunks(file_path, chunk_size=500):
    """
    Load a PDF file and split it into text chunks.
    Args:
        file_path (str): Path to the PDF file.
        chunk_size (int): Size of each text chunk.
    Returns:
        List[str]: List of text chunks.
    """
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    # Clean and split into chunks
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    return chunks
