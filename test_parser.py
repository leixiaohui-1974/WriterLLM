from docx import Document
from src.parser import parse_document
import io

# Create a dummy docx in memory
doc = Document()
doc.add_paragraph("Hello World from Docx")
doc_io = io.BytesIO()
doc.save(doc_io)
doc_io.seek(0)
doc_io.name = "test.docx"

text = parse_document(doc_io)
print(f"Docx Text: {text}")

assert "Hello World from Docx" in text
print("Parser Test Passed")
