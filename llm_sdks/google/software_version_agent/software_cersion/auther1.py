from pathlib import Path
from pypdf import PdfReader
from google.adk.tools import function_tool

def get_author(path: str) -> str:
    """Extract the author name from a PDF file's metadata."""

    pdf_path = Path(path)

    if not pdf_path.is_absolute():
        pdf_path = Path(__file__).parent / pdf_path

    if not pdf_path.exists():
        return f"PDF file not found: {pdf_path}"

    reader = PdfReader("sample_ai_author.pdf")
    metadata = reader.metadata

    if metadata and metadata.author:
        return metadata.author

    return "Author name not found in PDF metadata"

custom_tool=function_tool(func=get_author)