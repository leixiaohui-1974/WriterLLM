import io
import docx
import pypdf

def extract_text_from_docx(file_stream):
    """
    Extracts text from a .docx file stream.
    """
    doc = docx.Document(file_stream)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text)
    return "\n".join(full_text)

def extract_text_from_pdf(file_stream):
    """
    Extracts text from a .pdf file stream using pypdf.
    """
    reader = pypdf.PdfReader(file_stream)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    return "\n".join(full_text)

def parse_document(uploaded_file):
    """
    Parses a Streamlit UploadedFile object (or generic file object with .name attribute)
    and returns the extracted text.
    """
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == 'docx':
        return extract_text_from_docx(uploaded_file)
    elif file_type == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
