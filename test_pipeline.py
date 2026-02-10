"""End-to-end pipeline integration tests."""
import os
import shutil
import io
import pytest
import docx

from src.parser import parse_document
from src.generator import generate_slides
from src.models import SlideData, SlideTheme, Language
from src.renderer import create_pptx_file, create_slide_images, create_pdf_from_images


OUTPUT_DIR = "test_output"


@pytest.fixture(autouse=True)
def clean_output():
    """Clean test output directory before and after each test."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    yield
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)


def _create_test_docx():
    """Create a test DOCX document in memory."""
    doc = docx.Document()
    doc.add_heading("AI in Healthcare", 0)
    doc.add_paragraph("AI is revolutionizing healthcare diagnostics.")
    doc.add_paragraph("Machine learning models can predict diseases early.")
    doc.add_paragraph("Robotic surgery is becoming more precise.")
    doc.add_paragraph("Drug discovery is accelerated by AI algorithms.")
    doc.add_paragraph("Patient monitoring systems use AI for early detection.")
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    buf.name = "test_doc.docx"
    return buf


class TestFullPipeline:
    def test_parse_generate_render(self):
        """Test the complete pipeline: parse -> generate -> render."""
        # 1. Parse
        doc_io = _create_test_docx()
        text = parse_document(doc_io)
        assert "AI is revolutionizing" in text

        # 2. Generate Content (Mock)
        slides_data = generate_slides(text, num_slides=3)
        assert len(slides_data) == 3
        for s in slides_data:
            assert isinstance(s, SlideData)

        # 3. Render PPTX
        pptx_path = os.path.join(OUTPUT_DIR, "test.pptx")
        create_pptx_file(slides_data, pptx_path)
        assert os.path.exists(pptx_path)
        assert os.path.getsize(pptx_path) > 0

        # 4. Render Slide Images
        images_dir = os.path.join(OUTPUT_DIR, "images")
        image_paths = create_slide_images(slides_data, images_dir)
        assert len(image_paths) == 3
        for p in image_paths:
            assert os.path.exists(p)
            assert os.path.getsize(p) > 0

        # 5. Render PDF
        pdf_path = os.path.join(OUTPUT_DIR, "test.pdf")
        create_pdf_from_images(image_paths, pdf_path)
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0


class TestThemeRendering:
    def test_all_themes_render(self):
        """Verify that all themes produce valid output."""
        slides_data = generate_slides("Test content for theme rendering. " * 20, num_slides=2)

        for theme in SlideTheme:
            images_dir = os.path.join(OUTPUT_DIR, f"images_{theme.value}")
            image_paths = create_slide_images(slides_data, images_dir, theme=theme)
            assert len(image_paths) == 2
            for p in image_paths:
                assert os.path.exists(p)
                assert os.path.getsize(p) > 0


class TestMultiLanguage:
    def test_chinese_content_generation(self):
        text = "人工智能正在改变世界。它在医疗和金融领域广泛应用。机器学习是人工智能的重要分支。"
        slides = generate_slides(text, num_slides=2, language=Language.CHINESE)
        assert len(slides) == 2

    def test_english_content_generation(self):
        text = "Artificial Intelligence is transforming the world. It is used in many fields."
        slides = generate_slides(text, num_slides=2, language=Language.ENGLISH)
        assert len(slides) == 2


class TestModels:
    def test_slide_data_to_dict(self):
        slide = SlideData(title="Test", content=["A", "B"], speaker_notes="Notes", image_prompt="Prompt")
        d = slide.to_dict()
        assert d["title"] == "Test"
        assert d["content"] == ["A", "B"]

    def test_slide_data_from_dict(self):
        d = {"title": "Test", "content": ["A"], "speaker_notes": "Notes", "image_prompt": "Prompt"}
        slide = SlideData.from_dict(d)
        assert slide.title == "Test"
        assert slide.content == ["A"]

    def test_slide_data_from_dict_defaults(self):
        slide = SlideData.from_dict({})
        assert slide.title == "Untitled"
        assert slide.content == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
