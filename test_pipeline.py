import os
import shutil
import io
import docx
from src.parser import parse_document
from src.generator import generate_slides
from src.renderer import create_pptx_file, create_slide_images, create_pdf_from_images
from src.video import create_video_presentation

def test_pipeline():
    print("Starting pipeline test...")

    # 1. Create dummy docx
    doc = docx.Document()
    doc.add_heading('AI in Healthcare', 0)
    doc.add_paragraph('AI is revolutionizing healthcare diagnostics.')
    doc.add_paragraph('Machine learning models can predict diseases early.')
    doc.add_paragraph('Robotic surgery is becoming more precise.')

    # Save to BytesIO to simulate file upload
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    doc_io.name = "test_doc.docx"

    # 2. Parse
    print("Parsing document...")
    text = parse_document(doc_io)
    assert "AI is revolutionizing" in text

    # 3. Generate Content (Mock)
    print("Generating content...")
    slides_data = generate_slides(text, num_slides=3)
    assert len(slides_data) == 3

    # 4. Render Artifacts
    print("Rendering artifacts...")
    output_dir = "test_output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    pptx_path = os.path.join(output_dir, "test.pptx")
    create_pptx_file(slides_data, pptx_path)
    assert os.path.exists(pptx_path)

    images_dir = os.path.join(output_dir, "images")
    image_paths = create_slide_images(slides_data, images_dir)
    assert len(image_paths) == 3

    pdf_path = os.path.join(output_dir, "test.pdf")
    create_pdf_from_images(image_paths, pdf_path)
    assert os.path.exists(pdf_path)

    # 5. Generate Video
    print("Generating video...")
    video_path = os.path.join(output_dir, "test.mp4")
    scripts = [s.get("speaker_notes", "") for s in slides_data]
    create_video_presentation(image_paths, scripts, video_path)

    assert os.path.exists(video_path)
    print("Video generated successfully.")

    print("Pipeline Test Passed!")

if __name__ == "__main__":
    test_pipeline()
