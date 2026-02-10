"""End-to-end pipeline integration tests."""
import os
import shutil
import io
import pytest
import docx

from src.parser import parse_document
from src.generator import generate_slides
from src.models import SlideData, SlideLayout, SlideTheme, Language, ExportFormat, PresentationConfig
from src.renderer import create_pptx_file, create_slide_images, create_pdf_from_images
from src.image_gen import generate_slide_image, generate_slide_images_batch


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
        doc_io = _create_test_docx()
        text = parse_document(doc_io)
        assert "AI is revolutionizing" in text

        slides_data = generate_slides(text, num_slides=3)
        assert len(slides_data) == 3
        for s in slides_data:
            assert isinstance(s, SlideData)

        pptx_path = os.path.join(OUTPUT_DIR, "test.pptx")
        create_pptx_file(slides_data, pptx_path)
        assert os.path.exists(pptx_path)
        assert os.path.getsize(pptx_path) > 0

        images_dir = os.path.join(OUTPUT_DIR, "images")
        image_paths = create_slide_images(slides_data, images_dir)
        assert len(image_paths) == 3
        for p in image_paths:
            assert os.path.exists(p)
            assert os.path.getsize(p) > 0

        pdf_path = os.path.join(OUTPUT_DIR, "test.pdf")
        create_pdf_from_images(image_paths, pdf_path)
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0

    def test_themed_pptx_generation(self):
        """Test that themed PPTX files are created successfully."""
        slides_data = generate_slides("Test content. " * 20, num_slides=3)
        for theme in SlideTheme:
            path = os.path.join(OUTPUT_DIR, f"test_{theme.value}.pptx")
            create_pptx_file(slides_data, path, theme=theme)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0


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


class TestLayoutRendering:
    def test_all_layout_types_render(self):
        """Verify that all layout types render correctly."""
        slides_data = [
            SlideData(title="Title Slide", content=["Subtitle here"], layout=SlideLayout.TITLE,
                      speaker_notes="Welcome", image_prompt="Title visual"),
            SlideData(title="Content Slide", content=["Point 1", "Point 2", "Point 3"], layout=SlideLayout.CONTENT,
                      speaker_notes="Content notes", image_prompt="Content visual"),
            SlideData(title="Section Break", content=[], layout=SlideLayout.SECTION,
                      speaker_notes="Section notes", image_prompt="Section visual"),
            SlideData(title="Comparison", content=["Left 1", "Left 2", "Right 1", "Right 2"],
                      layout=SlideLayout.TWO_COLUMN, speaker_notes="Comparison notes", image_prompt="Compare visual"),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_layouts")
        image_paths = create_slide_images(slides_data, images_dir)
        assert len(image_paths) == 4
        for p in image_paths:
            assert os.path.exists(p)
            assert os.path.getsize(p) > 0

    def test_layout_pptx_rendering(self):
        """Verify PPTX rendering with different layouts."""
        slides_data = [
            SlideData(title="Title Slide", content=["Subtitle"], layout=SlideLayout.TITLE,
                      speaker_notes="Welcome"),
            SlideData(title="Content", content=["A", "B"], layout=SlideLayout.CONTENT,
                      speaker_notes="Content notes"),
            SlideData(title="Section", content=[], layout=SlideLayout.SECTION,
                      speaker_notes="Section notes"),
        ]
        pptx_path = os.path.join(OUTPUT_DIR, "layouts.pptx")
        create_pptx_file(slides_data, pptx_path)
        assert os.path.exists(pptx_path)
        assert os.path.getsize(pptx_path) > 0


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
        assert "layout" in d

    def test_slide_data_from_dict(self):
        d = {"title": "Test", "content": ["A"], "speaker_notes": "Notes", "image_prompt": "Prompt"}
        slide = SlideData.from_dict(d)
        assert slide.title == "Test"
        assert slide.content == ["A"]

    def test_slide_data_from_dict_defaults(self):
        slide = SlideData.from_dict({})
        assert slide.title == "Untitled"
        assert slide.content == []
        assert slide.layout == SlideLayout.CONTENT

    def test_slide_data_from_dict_with_layout(self):
        d = {"title": "Test", "layout": "title"}
        slide = SlideData.from_dict(d)
        assert slide.layout == SlideLayout.TITLE

    def test_slide_data_from_dict_invalid_layout(self):
        d = {"title": "Test", "layout": "nonexistent"}
        slide = SlideData.from_dict(d)
        assert slide.layout == SlideLayout.CONTENT

    def test_presentation_config_defaults(self):
        config = PresentationConfig()
        assert config.num_slides == 5
        assert config.language == Language.ENGLISH
        assert ExportFormat.PPTX in config.export_formats
        assert ExportFormat.VIDEO in config.export_formats

    def test_presentation_config_voice_name(self):
        config = PresentationConfig(language=Language.CHINESE, voice_gender="Female")
        assert "zh-CN" in config.voice_name

    def test_export_format_enum(self):
        assert ExportFormat.PPTX.value == "pptx"
        assert ExportFormat.PDF.value == "pdf"
        assert ExportFormat.VIDEO.value == "video"


class TestImageGen:
    def test_no_api_key_returns_none(self):
        result = generate_slide_image("test prompt", "/tmp/test.png")
        assert result is None

    def test_batch_no_api_key_returns_empty(self):
        prompts = [(0, "prompt 1"), (1, "prompt 2")]
        results = generate_slide_images_batch(prompts, OUTPUT_DIR)
        assert results == {}


class TestPdfGeneration:
    def test_empty_image_list_raises(self):
        with pytest.raises(ValueError, match="No images"):
            create_pdf_from_images([], os.path.join(OUTPUT_DIR, "empty.pdf"))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
