from pypdf import PdfReader

def load_pdf(path: str) -> str:
    """
    Load text from a PDF file.
    """
    reader = PdfReader(path)
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n".join(pages)

#Converts PDFs → raw text
#Handles multi-page documents