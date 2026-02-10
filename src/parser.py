"""
Document parsing module - extracts text from various document formats.
Supports: DOCX, PDF, TXT, Markdown.
"""
import logging
from typing import BinaryIO

import docx

pypdf = None  # lazy import to avoid cryptography issues in some environments

logger = logging.getLogger(__name__)

# Supported file extensions
SUPPORTED_EXTENSIONS = {"docx", "pdf", "txt", "md"}


def extract_text_from_docx(file_stream: BinaryIO) -> str:
    """Extract text from a .docx file stream, preserving paragraph structure."""
    doc = docx.Document(file_stream)
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            if para.style and para.style.name.startswith("Heading"):
                level = para.style.name.replace("Heading", "").strip()
                try:
                    level = int(level)
                except ValueError:
                    level = 1
                paragraphs.append(f"{'#' * level} {text}")
            else:
                paragraphs.append(text)
    return "\n\n".join(paragraphs)


def extract_text_from_pdf(file_stream: BinaryIO) -> str:
    """Extract text from a .pdf file stream using pypdf."""
    try:
        import pypdf as _pypdf
    except BaseException:
        raise ImportError("pypdf is not available. Install it with: pip install pypdf")
    reader = _pypdf.PdfReader(file_stream)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append(text.strip())
        else:
            logger.warning("Page %d: no extractable text found", i + 1)
    if not pages:
        raise ValueError("PDF contains no extractable text. It may be image-based.")
    return "\n\n".join(pages)


def extract_text_from_txt(file_stream: BinaryIO) -> str:
    """Extract text from a plain text file."""
    content = file_stream.read()
    if isinstance(content, bytes):
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            logger.warning("UTF-8 decode failed, falling back to latin-1")
            return content.decode("latin-1")
    return content


def extract_text_from_markdown(file_stream: BinaryIO) -> str:
    """Extract text from a Markdown file (kept as-is for structure)."""
    return extract_text_from_txt(file_stream)


def parse_document(uploaded_file) -> str:
    """
    Parse an uploaded file and return extracted text.

    Args:
        uploaded_file: A file-like object with a .name attribute
                      (e.g., Streamlit UploadedFile).

    Returns:
        Extracted text content as a string.

    Raises:
        ValueError: If the file type is unsupported or parsing fails.
    """
    filename = getattr(uploaded_file, "name", "")
    if not filename:
        raise ValueError("File has no name attribute; cannot determine type.")

    file_type = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    logger.info("Parsing document: %s (type: %s)", filename, file_type)

    if file_type not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: .{file_type}. "
            f"Supported: {', '.join('.' + ext for ext in sorted(SUPPORTED_EXTENSIONS))}"
        )

    extractors = {
        "docx": extract_text_from_docx,
        "pdf": extract_text_from_pdf,
        "txt": extract_text_from_txt,
        "md": extract_text_from_markdown,
    }

    text = extractors[file_type](uploaded_file)
    if not text or not text.strip():
        raise ValueError(f"No text content extracted from {filename}.")

    logger.info("Extracted %d characters from %s", len(text), filename)
    return text
