"""End-to-end pipeline integration tests."""
import os
import shutil
import io
import pytest
import docx

from pptx import Presentation
from pptx.util import Inches
from pptx.dml.color import RGBColor

from src.parser import parse_document
from src.generator import generate_slides
from src.models import SlideData, SlideLayout, SlideTheme, Language, ExportFormat, PresentationConfig
from src.renderer import (
    create_pptx_file, create_slide_images, create_pdf_from_images,
    _prepare_background, _get_font, _is_cjk_char, _contains_cjk,
    _wrap_text, _text_pixel_width, _draw_text, _draw_slide_footer,
    _compute_content_font_size, _estimate_content_lines, _cover_crop,
    _draw_gradient_rect, _fit_title_in_header, _draw_header_gradient,
    _set_pptx_slide_background, _add_pptx_slide_transition,
    _add_pptx_slide_number, _BULLET_ICONS, _format_pptx_bullet,
    CONTENT_MAX_WIDTH, CONTENT_FONT_SIZE, FOOTER_AREA, CONTENT_START_Y,
    SLIDE_HEIGHT, SLIDE_WIDTH, HEADER_HEIGHT, TITLE_FONT_SIZE,
)
from src.image_gen import generate_slide_image, generate_slide_images_batch
from src.models import ThemeColors, THEMES, serialize_project, deserialize_project
from src.generator import mock_generate_content, _create_toc_slide, _TOC_TITLES, _SUMMARY_TITLES, _build_speaker_notes, _TRANSITION_PHRASES, _CLOSING_PHRASES, _EMPHASIS_CONNECTORS, validate_content, _extract_json
from src.video import generate_srt_subtitles, _format_srt_timestamp
from src.renderer import _add_pptx_entrance_animations, _add_pptx_header_bar, _add_pptx_progress_bar, _compute_pptx_font_size, PPTX_TRANSITION_TYPES


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


def _create_test_bg_image(path):
    """Create a test background image."""
    from PIL import Image
    img = Image.new("RGB", (1920, 1080), color=(100, 150, 200))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    img.save(path, "PNG")
    return path


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


class TestBackgroundImageCompositing:
    """Tests for AI background image compositing into slides."""

    def test_slide_images_with_background(self):
        """Verify that background images are composited into slide images."""
        slides_data = [
            SlideData(title="Slide 1", content=["Content A"], layout=SlideLayout.CONTENT),
            SlideData(title="Slide 2", content=["Content B"], layout=SlideLayout.TITLE),
        ]
        # Create a fake background image
        bg_path = os.path.join(OUTPUT_DIR, "bg_000.png")
        _create_test_bg_image(bg_path)

        background_images = {0: bg_path}  # Only slide 0 has a background

        images_dir = os.path.join(OUTPUT_DIR, "images_bg")
        image_paths = create_slide_images(
            slides_data, images_dir, background_images=background_images,
        )
        assert len(image_paths) == 2
        for p in image_paths:
            assert os.path.exists(p)
            # Files with bg should have content
            assert os.path.getsize(p) > 0

    def test_pptx_with_background(self):
        """Verify PPTX generation with background images."""
        slides_data = [
            SlideData(title="BG Slide", content=["Test"], layout=SlideLayout.CONTENT),
        ]
        bg_path = os.path.join(OUTPUT_DIR, "bg_pptx.png")
        _create_test_bg_image(bg_path)

        pptx_path = os.path.join(OUTPUT_DIR, "bg_test.pptx")
        create_pptx_file(
            slides_data, pptx_path,
            background_images={0: bg_path},
        )
        assert os.path.exists(pptx_path)
        assert os.path.getsize(pptx_path) > 0

    def test_prepare_background_with_image(self):
        """Test _prepare_background composites correctly."""
        bg_path = os.path.join(OUTPUT_DIR, "bg_prep.png")
        _create_test_bg_image(bg_path)

        colors = THEMES[SlideTheme.PROFESSIONAL]
        img = _prepare_background(0, colors, background_images={0: bg_path})
        assert img.size == (1920, 1080)
        assert img.mode == "RGB"

    def test_prepare_background_without_image(self):
        """Test _prepare_background returns solid color without image."""
        colors = THEMES[SlideTheme.DARK]
        img = _prepare_background(0, colors, background_images=None)
        assert img.size == (1920, 1080)
        # Should be the dark theme background color
        pixel = img.getpixel((100, 100))
        assert pixel == colors.background

    def test_all_layouts_with_background(self):
        """Verify all layout types render correctly with background images."""
        slides_data = [
            SlideData(title="Title", content=["Sub"], layout=SlideLayout.TITLE),
            SlideData(title="Content", content=["A", "B"], layout=SlideLayout.CONTENT),
            SlideData(title="Section", content=[], layout=SlideLayout.SECTION),
            SlideData(title="Two Col", content=["L1", "L2", "R1", "R2"], layout=SlideLayout.TWO_COLUMN),
        ]
        bg_dir = os.path.join(OUTPUT_DIR, "bgs")
        os.makedirs(bg_dir, exist_ok=True)
        bg_images = {}
        for i in range(4):
            bg_path = os.path.join(bg_dir, f"bg_{i}.png")
            _create_test_bg_image(bg_path)
            bg_images[i] = bg_path

        images_dir = os.path.join(OUTPUT_DIR, "images_all_bg")
        image_paths = create_slide_images(
            slides_data, images_dir, background_images=bg_images,
        )
        assert len(image_paths) == 4
        for p in image_paths:
            assert os.path.exists(p)


class TestCJKTextWrapping:
    """Tests for CJK character detection and pixel-based text wrapping."""

    def test_is_cjk_char_chinese(self):
        assert _is_cjk_char("人") is True
        assert _is_cjk_char("智") is True

    def test_is_cjk_char_japanese(self):
        assert _is_cjk_char("あ") is True  # Hiragana
        assert _is_cjk_char("カ") is True  # Katakana

    def test_is_cjk_char_korean(self):
        assert _is_cjk_char("한") is True  # Hangul

    def test_is_cjk_char_latin(self):
        assert _is_cjk_char("A") is False
        assert _is_cjk_char("z") is False
        assert _is_cjk_char(" ") is False

    def test_contains_cjk(self):
        assert _contains_cjk("人工智能") is True
        assert _contains_cjk("Hello World") is False
        assert _contains_cjk("Hello 世界") is True  # Mixed
        assert _contains_cjk("") is False

    def test_wrap_text_latin(self):
        font = _get_font("DejaVuSans.ttf", 45, Language.ENGLISH)
        result = _wrap_text("Short text", font, 1720)
        assert len(result) >= 1
        assert "Short text" in result[0]

    def test_wrap_text_cjk_wraps_long_string(self):
        """CJK text without spaces must be wrapped by pixel width."""
        font = _get_font("DejaVuSans.ttf", 45, Language.CHINESE)
        long_cjk = "人工智能正在改变世界的方方面面包括医疗金融教育交通等各个领域"
        result = _wrap_text(long_cjk, font, 800)  # Narrow width
        assert len(result) >= 2, f"Expected multiple lines, got {len(result)}: {result}"

    def test_wrap_text_cjk_short_fits(self):
        """Short CJK text should fit in one line."""
        font = _get_font("DejaVuSans.ttf", 45, Language.CHINESE)
        result = _wrap_text("人工智能", font, 1720)
        assert len(result) == 1

    def test_wrap_text_empty(self):
        font = _get_font("DejaVuSans.ttf", 45, Language.ENGLISH)
        assert _wrap_text("", font, 1000) == []
        assert _wrap_text("   ", font, 1000) == []

    def test_wrap_text_mixed_cjk_latin(self):
        """Mixed CJK+Latin text should wrap correctly."""
        font = _get_font("DejaVuSans.ttf", 45, Language.CHINESE)
        mixed = "AI人工智能is changing the world世界"
        result = _wrap_text(mixed, font, 600)
        assert len(result) >= 1

    def test_text_pixel_width(self):
        font = _get_font("DejaVuSans.ttf", 45, Language.ENGLISH)
        assert _text_pixel_width("", font) == 0
        w = _text_pixel_width("Hello", font)
        assert w > 0
        # Longer text should be wider
        w2 = _text_pixel_width("Hello World", font)
        assert w2 > w


class TestCJKFontSupport:
    """Tests for CJK font loading and rendering."""

    def test_cjk_font_loading_chinese(self):
        font = _get_font("DejaVuSans.ttf", 45, Language.CHINESE)
        assert font is not None

    def test_cjk_font_loading_japanese(self):
        font = _get_font("DejaVuSans.ttf", 45, Language.JAPANESE)
        assert font is not None

    def test_cjk_font_loading_korean(self):
        font = _get_font("DejaVuSans.ttf", 45, Language.KOREAN)
        assert font is not None

    def test_english_font_loading(self):
        font = _get_font("DejaVuSans.ttf", 45, Language.ENGLISH)
        assert font is not None

    def test_chinese_slide_rendering(self):
        """Verify Chinese text renders without error."""
        slides_data = [
            SlideData(title="人工智能", content=["机器学习", "深度学习"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_zh")
        image_paths = create_slide_images(
            slides_data, images_dir, language=Language.CHINESE,
        )
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_japanese_slide_rendering(self):
        """Verify Japanese text renders without error."""
        slides_data = [
            SlideData(title="プレゼンテーション", content=["ポイント1", "ポイント2"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_ja")
        image_paths = create_slide_images(
            slides_data, images_dir, language=Language.JAPANESE,
        )
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_chinese_section_layout(self):
        """Verify section layout renders CJK title with correct font."""
        slides_data = [
            SlideData(title="第二部分", content=[], layout=SlideLayout.SECTION),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_zh_section")
        image_paths = create_slide_images(
            slides_data, images_dir, language=Language.CHINESE,
        )
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_cjk_long_content_wrapping(self):
        """Verify long Chinese text wraps correctly in slide images."""
        long_text = "人工智能正在改变世界的方方面面包括医疗金融教育交通等各个领域，它能够帮助我们更好地理解和分析大量数据"
        slides_data = [
            SlideData(title="长文本测试", content=[long_text], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_zh_long")
        image_paths = create_slide_images(
            slides_data, images_dir, language=Language.CHINESE,
        )
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0


class TestTextShadow:
    """Tests for text shadow rendering with background images."""

    def test_slide_with_bg_renders_shadow(self):
        """Verify slides with background images render without error (shadow active)."""
        slides_data = [
            SlideData(title="Shadow Test", content=["Point A", "Point B"], layout=SlideLayout.CONTENT),
        ]
        bg_path = os.path.join(OUTPUT_DIR, "bg_shadow.png")
        _create_test_bg_image(bg_path)

        images_dir = os.path.join(OUTPUT_DIR, "images_shadow")
        image_paths = create_slide_images(
            slides_data, images_dir, background_images={0: bg_path},
        )
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_draw_text_with_shadow(self):
        """Verify _draw_text with shadow draws more dark pixels than without."""
        from PIL import Image, ImageDraw
        # Render without shadow
        img_no_shadow = Image.new("RGB", (400, 100), (255, 255, 255))
        draw1 = ImageDraw.Draw(img_no_shadow)
        font = _get_font("DejaVuSans.ttf", 30, Language.ENGLISH)
        _draw_text(draw1, (10, 10), "Shadow", font, (255, 0, 0), shadow=False)
        px1 = img_no_shadow.load()
        dark_no_shadow = sum(1 for x in range(400) for y in range(100) if px1[x, y][0] < 200)

        # Render with shadow
        img_shadow = Image.new("RGB", (400, 100), (255, 255, 255))
        draw2 = ImageDraw.Draw(img_shadow)
        _draw_text(draw2, (10, 10), "Shadow", font, (255, 0, 0), shadow=True)
        px2 = img_shadow.load()
        dark_shadow = sum(1 for x in range(400) for y in range(100) if px2[x, y][0] < 200)

        # Shadow version should have more dark pixels (the black shadow layer)
        assert dark_shadow > dark_no_shadow, "Shadow should add more dark pixels"


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


class TestResponsiveFontSizing:
    """Tests for responsive font sizing when content overflows."""

    def test_compute_font_size_short_content(self):
        """Short content should use the base font size."""
        content = ["Point 1", "Point 2"]
        available_h = SLIDE_HEIGHT - CONTENT_START_Y - FOOTER_AREA
        size = _compute_content_font_size(content, Language.ENGLISH, CONTENT_MAX_WIDTH, available_h)
        assert size == CONTENT_FONT_SIZE

    def test_compute_font_size_long_content_shrinks(self):
        """Many bullet points should trigger font shrinking."""
        content = [f"This is bullet point number {i} with enough text to be meaningful" for i in range(15)]
        available_h = SLIDE_HEIGHT - CONTENT_START_Y - FOOTER_AREA
        size = _compute_content_font_size(content, Language.ENGLISH, CONTENT_MAX_WIDTH, available_h)
        assert size < CONTENT_FONT_SIZE
        assert size >= 24  # Should not go below minimum

    def test_compute_font_size_minimum_bound(self):
        """Even very long content should not go below minimum font size."""
        content = [f"Very long line {i}" for i in range(50)]
        available_h = 200  # Very limited height
        size = _compute_content_font_size(content, Language.ENGLISH, CONTENT_MAX_WIDTH, available_h)
        assert size >= 24

    def test_estimate_content_lines(self):
        """Verify line estimation works for simple content."""
        font = _get_font("DejaVuSans.ttf", 45, Language.ENGLISH)
        lines = _estimate_content_lines(["Short", "Also short"], font, CONTENT_MAX_WIDTH)
        assert lines == 2

    def test_estimate_content_lines_wrapping(self):
        """Long text should produce more estimated lines."""
        font = _get_font("DejaVuSans.ttf", 45, Language.ENGLISH)
        long_text = "This is a very long sentence that should definitely wrap around multiple times " * 3
        lines = _estimate_content_lines([long_text], font, CONTENT_MAX_WIDTH)
        assert lines >= 2

    def test_responsive_rendering_many_bullets(self):
        """Verify slide with many bullets renders without error using smaller font."""
        slides_data = [
            SlideData(
                title="Dense Content",
                content=[f"Bullet point {i}: description of item" for i in range(12)],
                layout=SlideLayout.CONTENT,
            ),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_responsive")
        image_paths = create_slide_images(slides_data, images_dir)
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_responsive_two_column_rendering(self):
        """Verify two-column layout with many items uses responsive sizing."""
        slides_data = [
            SlideData(
                title="Dense Two Column",
                content=[f"Item {i}" for i in range(14)],
                layout=SlideLayout.TWO_COLUMN,
            ),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_responsive_2col")
        image_paths = create_slide_images(slides_data, images_dir)
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0


class TestCoverCrop:
    """Tests for aspect-ratio-preserving background image resizing."""

    def test_cover_crop_landscape(self):
        from PIL import Image
        img = Image.new("RGBA", (2000, 1000), (100, 100, 100, 255))
        cropped = _cover_crop(img, 1920, 1080)
        assert cropped.size == (1920, 1080)

    def test_cover_crop_portrait(self):
        from PIL import Image
        img = Image.new("RGBA", (800, 1200), (100, 100, 100, 255))
        cropped = _cover_crop(img, 1920, 1080)
        assert cropped.size == (1920, 1080)

    def test_cover_crop_square(self):
        from PIL import Image
        img = Image.new("RGBA", (1000, 1000), (100, 100, 100, 255))
        cropped = _cover_crop(img, 1920, 1080)
        assert cropped.size == (1920, 1080)


class TestConfigurableOverlay:
    """Tests for configurable background overlay opacity."""

    def test_overlay_opacity_default(self):
        """Default overlay opacity should work."""
        bg_path = os.path.join(OUTPUT_DIR, "bg_opacity.png")
        _create_test_bg_image(bg_path)
        colors = THEMES[SlideTheme.PROFESSIONAL]
        img = _prepare_background(0, colors, {0: bg_path})
        assert img.size == (1920, 1080)

    def test_overlay_opacity_transparent(self):
        """Fully transparent overlay should show more of the original image."""
        bg_path = os.path.join(OUTPUT_DIR, "bg_transparent.png")
        _create_test_bg_image(bg_path)
        colors = THEMES[SlideTheme.PROFESSIONAL]
        img_transparent = _prepare_background(0, colors, {0: bg_path}, overlay_opacity=0)
        img_opaque = _prepare_background(0, colors, {0: bg_path}, overlay_opacity=200)
        # Both should be valid images
        assert img_transparent.size == (1920, 1080)
        assert img_opaque.size == (1920, 1080)
        # Transparent should be closer to original BG color (100,150,200)
        px_t = img_transparent.getpixel((500, 500))
        px_o = img_opaque.getpixel((500, 500))
        # More opaque = closer to theme background (255,255,255 for Professional)
        assert px_o[0] > px_t[0] or px_o[1] > px_t[1]

    def test_overlay_opacity_in_slide_images(self):
        """Verify overlay_opacity parameter works in create_slide_images."""
        slides_data = [
            SlideData(title="Opacity Test", content=["Test"], layout=SlideLayout.CONTENT),
        ]
        bg_path = os.path.join(OUTPUT_DIR, "bg_slide_opacity.png")
        _create_test_bg_image(bg_path)
        images_dir = os.path.join(OUTPUT_DIR, "images_opacity")
        image_paths = create_slide_images(
            slides_data, images_dir,
            background_images={0: bg_path},
            overlay_opacity=100,
        )
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0


class TestMockSummarySlide:
    """Tests for improved mock mode with summary slide generation."""

    def test_mock_generates_summary_slide(self):
        """Mock mode with 5+ slides should produce summary + TOC slides."""
        text = "AI is transforming healthcare. Machine learning improves diagnostics. " * 20
        slides = mock_generate_content(text, num_slides=5)
        # 5 content/summary slides + 1 TOC inserted at position 1 = 6
        assert len(slides) == 6
        last = slides[-1]
        assert last.title == "Key Takeaways"
        # TOC should be at index 1
        assert slides[1].title == "Agenda"

    def test_mock_summary_chinese(self):
        """Chinese mock mode should produce Chinese summary and TOC titles."""
        text = "人工智能正在改变世界。机器学习改善诊断。" * 10
        slides = mock_generate_content(text, num_slides=5, language=Language.CHINESE)
        last = slides[-1]
        assert last.title == "\u6838\u5fc3\u8981\u70b9"
        # Chinese TOC title
        assert slides[1].title == "\u76ee\u5f55"

    def test_mock_no_summary_for_few_slides(self):
        """2 slides should not have a separate summary or TOC."""
        text = "Short content for testing."
        slides = mock_generate_content(text, num_slides=2)
        assert len(slides) == 2

    def test_mock_summary_has_content(self):
        """Summary slide should have content points from other slides."""
        text = "First topic is important. Second topic matters too. Third point is key. " * 10
        slides = mock_generate_content(text, num_slides=5)
        last = slides[-1]
        assert len(last.content) >= 1

    def test_mock_improved_sentence_splitting(self):
        """Verify new separators like semicolons and ellipses are handled."""
        text = "Point one; Point two\u2026 Point three\uff01"
        slides = mock_generate_content(text, num_slides=2)
        assert len(slides) == 2


class TestPresentationConfigOverlay:
    """Tests for PresentationConfig overlay_opacity field."""

    def test_config_default_overlay(self):
        config = PresentationConfig()
        assert config.overlay_opacity == 130

    def test_config_custom_overlay(self):
        config = PresentationConfig(overlay_opacity=200)
        assert config.overlay_opacity == 200


class TestGradientHeader:
    """Tests for gradient header rendering in v6."""

    def test_draw_gradient_rect_produces_gradient(self):
        """Verify gradient rectangle draws a smooth vertical gradient."""
        from PIL import Image
        img = Image.new("RGB", (200, 100), (255, 255, 255))
        _draw_gradient_rect(img, (0, 0, 200, 100), (0, 0, 0), (255, 255, 255))
        # Top row should be dark, bottom row should be light
        top_pixel = img.getpixel((100, 0))
        bottom_pixel = img.getpixel((100, 99))
        assert top_pixel[0] < 10  # near black
        assert bottom_pixel[0] > 240  # near white

    def test_draw_gradient_rect_single_row(self):
        """Gradient with h=1 should not crash."""
        from PIL import Image
        img = Image.new("RGB", (100, 1), (0, 0, 0))
        _draw_gradient_rect(img, (0, 0, 100, 1), (255, 0, 0), (0, 0, 255))
        assert img.getpixel((50, 0)) is not None

    def test_draw_header_gradient_fills_header_area(self):
        """Verify header gradient fills the header area with theme colors."""
        from PIL import Image
        img = Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), (255, 255, 255))
        colors = THEMES[SlideTheme.OCEAN]
        _draw_header_gradient(img, colors)
        # Top of header should be close to header color
        px = img.getpixel((100, 5))
        assert abs(px[0] - colors.header[0]) < 5
        assert abs(px[1] - colors.header[1]) < 5

    def test_gradient_header_in_content_slide(self):
        """Content slide should render with gradient header without error."""
        slides_data = [
            SlideData(title="Gradient Test", content=["Point 1", "Point 2"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_gradient")
        image_paths = create_slide_images(slides_data, images_dir, theme=SlideTheme.DARK)
        assert len(image_paths) == 1
        # Verify header area has dark theme gradient (not plain white)
        from PIL import Image
        img = Image.open(image_paths[0])
        header_px = img.getpixel((100, 10))
        assert header_px[0] < 100  # Dark theme header should be dark


class TestTitleWrapping:
    """Tests for responsive title wrapping in headers."""

    def test_short_title_no_wrapping(self):
        """Short title should fit in one line."""
        font = _get_font("DejaVuSans-Bold.ttf", TITLE_FONT_SIZE, Language.ENGLISH)
        lines, used_font = _fit_title_in_header("Short Title", font, Language.ENGLISH, CONTENT_MAX_WIDTH)
        assert len(lines) == 1
        assert "Short Title" in lines[0]

    def test_long_title_wraps(self):
        """Very long title should wrap into multiple lines."""
        font = _get_font("DejaVuSans-Bold.ttf", TITLE_FONT_SIZE, Language.ENGLISH)
        long_title = "This Is A Very Long Presentation Title That Should Definitely Wrap Into Multiple Lines"
        lines, used_font = _fit_title_in_header(long_title, font, Language.ENGLISH, CONTENT_MAX_WIDTH)
        assert len(lines) >= 1
        assert len(lines) <= 2  # Should be capped at 2 lines

    def test_title_font_shrinks_for_long_text(self):
        """Title font should shrink when text is very long."""
        font = _get_font("DejaVuSans-Bold.ttf", TITLE_FONT_SIZE, Language.ENGLISH)
        very_long = "Extremely Long Title " * 10
        lines, used_font = _fit_title_in_header(very_long, font, Language.ENGLISH, CONTENT_MAX_WIDTH)
        assert len(lines) <= 2

    def test_cjk_title_wrapping(self):
        """CJK titles should wrap correctly."""
        font = _get_font("DejaVuSans-Bold.ttf", TITLE_FONT_SIZE, Language.CHINESE)
        cjk_title = "人工智能在医疗健康领域的应用与发展前景展望分析报告"
        lines, used_font = _fit_title_in_header(cjk_title, font, Language.CHINESE, CONTENT_MAX_WIDTH)
        assert len(lines) >= 1

    def test_long_title_slide_renders(self):
        """Slide with a very long title should render without error."""
        slides_data = [
            SlideData(
                title="This Is An Exceptionally Long Title That Tests The Wrapping Feature in Content Slides",
                content=["Point A", "Point B"],
                layout=SlideLayout.CONTENT,
            ),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_long_title")
        image_paths = create_slide_images(slides_data, images_dir)
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0


class TestTOCSlide:
    """Tests for auto-generated table of contents / agenda slide."""

    def test_create_toc_slide_english(self):
        """TOC slide should have correct English title and content from slide titles."""
        slides = [
            SlideData(title="Introduction", content=["A"], layout=SlideLayout.CONTENT),
            SlideData(title="Methods", content=["B"], layout=SlideLayout.CONTENT),
            SlideData(title="Results", content=["C"], layout=SlideLayout.CONTENT),
        ]
        toc = _create_toc_slide(slides, Language.ENGLISH)
        assert toc.title == "Agenda"
        assert "Introduction" in toc.content
        assert "Methods" in toc.content
        assert toc.layout == SlideLayout.CONTENT

    def test_create_toc_slide_chinese(self):
        """Chinese TOC should use Chinese title."""
        slides = [SlideData(title="分析", content=["A"], layout=SlideLayout.CONTENT)]
        toc = _create_toc_slide(slides, Language.CHINESE)
        assert toc.title == "\u76ee\u5f55"

    def test_toc_skips_title_layout(self):
        """TOC should not include slides with TITLE layout."""
        slides = [
            SlideData(title="Cover Title", content=[], layout=SlideLayout.TITLE),
            SlideData(title="Real Content", content=["A"], layout=SlideLayout.CONTENT),
        ]
        toc = _create_toc_slide(slides, Language.ENGLISH)
        assert "Cover Title" not in toc.content
        assert "Real Content" in toc.content

    def test_toc_max_items(self):
        """TOC should have at most 8 items."""
        slides = [
            SlideData(title=f"Topic {i}", content=["X"], layout=SlideLayout.CONTENT)
            for i in range(12)
        ]
        toc = _create_toc_slide(slides, Language.ENGLISH)
        assert len(toc.content) <= 8

    def test_toc_titles_all_languages(self):
        """All supported languages should have a TOC title."""
        for lang in Language:
            assert lang in _TOC_TITLES

    def test_mock_inserts_toc_for_5_plus_slides(self):
        """Mock generation with 5+ slides should insert TOC at position 1."""
        text = "Point one. Point two. Point three. Point four. Point five. " * 10
        slides = mock_generate_content(text, num_slides=5)
        assert slides[0].layout == SlideLayout.TITLE
        assert slides[1].title == "Agenda"

    def test_mock_no_toc_for_few_slides(self):
        """Mock generation with <5 slides should not insert TOC."""
        text = "Short text for few slides."
        slides = mock_generate_content(text, num_slides=3)
        for s in slides:
            assert s.title != "Agenda"


class TestSpeakingRate:
    """Tests for TTS speaking rate configuration."""

    def test_config_default_speaking_rate(self):
        config = PresentationConfig()
        assert config.speaking_rate == "+0%"

    def test_config_custom_speaking_rate(self):
        config = PresentationConfig(speaking_rate="+20%")
        assert config.speaking_rate == "+20%"

    def test_config_negative_speaking_rate(self):
        config = PresentationConfig(speaking_rate="-10%")
        assert config.speaking_rate == "-10%"


class TestPPTXSlideBackground:
    """Tests for PPTX solid background fill (v6)."""

    def test_set_pptx_slide_background(self):
        """Setting a slide background should not raise."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(slide_layout)
        # Should not raise
        _set_pptx_slide_background(slide, (44, 62, 80))

    def test_pptx_themed_backgrounds(self):
        """PPTX generation with all themes should produce valid files with backgrounds."""
        slides_data = [
            SlideData(title="BG Test", content=["A"], layout=SlideLayout.TITLE),
            SlideData(title="Content", content=["B", "C"], layout=SlideLayout.CONTENT),
        ]
        for theme in SlideTheme:
            path = os.path.join(OUTPUT_DIR, f"bg_{theme.value}.pptx")
            create_pptx_file(slides_data, path, theme=theme)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0

    def test_pptx_all_layouts_with_background_colors(self):
        """All layout types should get background colors in PPTX."""
        slides_data = [
            SlideData(title="Title", content=["Sub"], layout=SlideLayout.TITLE),
            SlideData(title="Content", content=["A", "B"], layout=SlideLayout.CONTENT),
            SlideData(title="Section", content=[], layout=SlideLayout.SECTION),
            SlideData(title="Two Col", content=["L1", "L2", "R1", "R2"], layout=SlideLayout.TWO_COLUMN),
        ]
        pptx_path = os.path.join(OUTPUT_DIR, "bg_all_layouts.pptx")
        create_pptx_file(slides_data, pptx_path)
        assert os.path.exists(pptx_path)
        # Verify slides were created
        prs = Presentation(pptx_path)
        assert len(prs.slides) == 4


class TestPPTXTransitions:
    """Tests for PPTX slide transitions (v7)."""

    def test_transition_does_not_raise(self):
        """Adding a transition to a slide should not raise."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        _add_pptx_slide_transition(slide)

    def test_pptx_with_transitions(self):
        """PPTX generation should include transitions without error."""
        slides_data = [
            SlideData(title="Slide 1", content=["A"], layout=SlideLayout.TITLE),
            SlideData(title="Slide 2", content=["B", "C"], layout=SlideLayout.CONTENT),
            SlideData(title="Slide 3", content=[], layout=SlideLayout.SECTION),
        ]
        path = os.path.join(OUTPUT_DIR, "transitions.pptx")
        create_pptx_file(slides_data, path)
        assert os.path.exists(path)
        prs = Presentation(path)
        assert len(prs.slides) == 3


class TestPPTXSlideNumbers:
    """Tests for PPTX slide numbering and footer branding (v7)."""

    def test_slide_number_does_not_raise(self):
        """Adding slide numbers should not raise."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        colors = THEMES[SlideTheme.PROFESSIONAL]
        _add_pptx_slide_number(slide, 0, 3, colors)

    def test_slide_number_with_branding(self):
        """Slide numbers with company and author should not raise."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        colors = THEMES[SlideTheme.OCEAN]
        _add_pptx_slide_number(slide, 2, 5, colors, footer_company="ACME Corp", footer_author="Jane Doe")
        # Should have extra text boxes for branding
        text_shapes = [s for s in slide.shapes if s.has_text_frame]
        assert len(text_shapes) >= 3  # slide number + company + author

    def test_pptx_with_footer_branding(self):
        """PPTX file with footer branding should be valid."""
        slides_data = [
            SlideData(title="Branded", content=["Test"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "branded.pptx")
        create_pptx_file(slides_data, path, footer_company="Test Inc.", footer_author="Author")
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0


class TestBulletStyling:
    """Tests for themed bullet icons in slide images (v7)."""

    def test_bullet_icons_defined(self):
        """Bullet icon list should exist and be non-empty."""
        assert len(_BULLET_ICONS) > 0

    def test_bullet_in_content_slide(self):
        """Content slide with bullets should render with accent-colored icons."""
        slides_data = [
            SlideData(title="Bullet Test", content=["Point 1", "Point 2", "Point 3"],
                      layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_bullets")
        image_paths = create_slide_images(slides_data, images_dir, theme=SlideTheme.OCEAN)
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_bullet_in_two_column(self):
        """Two-column slide should also use themed bullets."""
        slides_data = [
            SlideData(title="Two Col Bullets", content=["A", "B", "C", "D"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_bullets_2col")
        image_paths = create_slide_images(slides_data, images_dir, theme=SlideTheme.SUNSET)
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0


class TestSectionSlideEnhanced:
    """Tests for enhanced section slide styling (v7)."""

    def test_section_slide_gradient(self):
        """Section slide should render with gradient background."""
        slides_data = [
            SlideData(title="Section Break", content=[], layout=SlideLayout.SECTION),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_section_v7")
        image_paths = create_slide_images(slides_data, images_dir, theme=SlideTheme.DARK)
        assert len(image_paths) == 1
        # Check that section slide has dark gradient (header color)
        from PIL import Image
        img = Image.open(image_paths[0])
        top_px = img.getpixel((100, 10))
        assert top_px[0] < 50  # Dark theme header should be very dark

    def test_section_slide_all_themes(self):
        """Section slides should render correctly across all themes."""
        slides_data = [
            SlideData(title="Theme Test", content=[], layout=SlideLayout.SECTION),
        ]
        for theme in SlideTheme:
            images_dir = os.path.join(OUTPUT_DIR, f"images_section_{theme.value}")
            image_paths = create_slide_images(slides_data, images_dir, theme=theme)
            assert len(image_paths) == 1
            assert os.path.getsize(image_paths[0]) > 0

    def test_section_with_background_image(self):
        """Section slide with background image should render without error."""
        slides_data = [
            SlideData(title="BG Section", content=[], layout=SlideLayout.SECTION),
        ]
        bg_path = os.path.join(OUTPUT_DIR, "bg_section.png")
        _create_test_bg_image(bg_path)
        images_dir = os.path.join(OUTPUT_DIR, "images_section_bg")
        image_paths = create_slide_images(
            slides_data, images_dir, background_images={0: bg_path},
        )
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0


class TestSpeakerNotesEnhanced:
    """Tests for improved mock speaker notes (v7)."""

    def test_build_speaker_notes_english(self):
        """English speaker notes should include transition phrases."""
        notes = _build_speaker_notes("AI Overview", ["Machine learning", "Deep learning"],
                                     0, 5, Language.ENGLISH)
        assert len(notes) > 0
        assert "AI Overview" in notes or "Machine learning" in notes

    def test_build_speaker_notes_chinese(self):
        """Chinese speaker notes should use Chinese phrases."""
        notes = _build_speaker_notes("AI\u6982\u8ff0", ["\u673a\u5668\u5b66\u4e60"],
                                     0, 5, Language.CHINESE)
        assert len(notes) > 0

    def test_build_speaker_notes_last_slide(self):
        """Last slide notes should use wrap-up phrasing."""
        notes = _build_speaker_notes("Summary", ["Point A"], 4, 5, Language.ENGLISH)
        assert "wrap up" in notes.lower() or "key points" in notes.lower()

    def test_mock_notes_have_transitions(self):
        """Mock-generated slides should have structured speaker notes."""
        text = "AI transforms healthcare. ML improves diagnostics. NLP reads records. " * 10
        slides = mock_generate_content(text, num_slides=5)
        for slide in slides:
            assert len(slide.speaker_notes) > 0

    def test_transition_phrases_all_languages(self):
        """Transition phrases should exist for key languages."""
        for lang in [Language.ENGLISH, Language.CHINESE, Language.JAPANESE]:
            assert lang in _TRANSITION_PHRASES
            assert len(_TRANSITION_PHRASES[lang]) >= 3


class TestFooterBranding:
    """Tests for footer branding in slide images (v7)."""

    def test_slide_images_with_company(self):
        """Slide images with company branding should render without error."""
        slides_data = [
            SlideData(title="Branded Slide", content=["A"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_branded")
        image_paths = create_slide_images(
            slides_data, images_dir, footer_company="ACME Corp",
        )
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_slide_images_with_full_branding(self):
        """Slide images with company + author should render correctly."""
        slides_data = [
            SlideData(title="Full Brand", content=["X", "Y"], layout=SlideLayout.CONTENT),
            SlideData(title="Title", content=["Sub"], layout=SlideLayout.TITLE),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_full_brand")
        image_paths = create_slide_images(
            slides_data, images_dir,
            footer_company="Test Corp", footer_author="John Smith",
        )
        assert len(image_paths) == 2
        for p in image_paths:
            assert os.path.getsize(p) > 0

    def test_config_footer_defaults(self):
        """PresentationConfig should have empty footer fields by default."""
        config = PresentationConfig()
        assert config.footer_company == ""
        assert config.footer_author == ""

    def test_config_footer_custom(self):
        """PresentationConfig should accept custom footer values."""
        config = PresentationConfig(footer_company="My Co", footer_author="Jane")
        assert config.footer_company == "My Co"
        assert config.footer_author == "Jane"

    def test_draw_slide_footer_function(self):
        """The _draw_slide_footer helper should not raise."""
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = _get_font("DejaVuSans.ttf", 30, Language.ENGLISH)
        colors = THEMES[SlideTheme.PROFESSIONAL]
        _draw_slide_footer(draw, font, colors, 0, 5, False, False,
                          footer_company="Test", footer_author="Author")


class TestFooterBrandingFlow:
    """Tests for footer branding actually flowing through to rendered images (v8 bugfix)."""

    def test_branding_renders_in_content_slide(self):
        """Footer company text should appear in rendered content slide image."""
        from PIL import Image
        slides_data = [
            SlideData(title="Flow Test", content=["A", "B"], layout=SlideLayout.CONTENT),
        ]
        # Render with and without branding, compare
        dir_no = os.path.join(OUTPUT_DIR, "images_no_brand")
        dir_yes = os.path.join(OUTPUT_DIR, "images_yes_brand")
        paths_no = create_slide_images(slides_data, dir_no)
        paths_yes = create_slide_images(slides_data, dir_yes,
                                        footer_company="ACME Corp", footer_author="Jane")
        img_no = Image.open(paths_no[0])
        img_yes = Image.open(paths_yes[0])
        # The branded image should differ from unbranded (footer area changed)
        px_no = [img_no.getpixel((200, SLIDE_HEIGHT - 40 + y)) for y in range(5)]
        px_yes = [img_yes.getpixel((200, SLIDE_HEIGHT - 40 + y)) for y in range(5)]
        assert px_no != px_yes, "Footer branding should change the rendered image"

    def test_branding_renders_in_title_slide(self):
        """Footer branding should also render in title slides."""
        slides_data = [
            SlideData(title="Title", content=["Sub"], layout=SlideLayout.TITLE),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_title_brand")
        paths = create_slide_images(slides_data, images_dir,
                                    footer_company="Corp", footer_author="Author")
        assert len(paths) == 1
        assert os.path.getsize(paths[0]) > 0

    def test_branding_renders_in_section_slide(self):
        """Footer branding should render in section slides."""
        slides_data = [
            SlideData(title="Section", content=[], layout=SlideLayout.SECTION),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_section_brand")
        paths = create_slide_images(slides_data, images_dir,
                                    footer_company="My Co")
        assert len(paths) == 1
        assert os.path.getsize(paths[0]) > 0


class TestNewThemes:
    """Tests for new themes added in v8 (Forest, Royal, Tech)."""

    def test_forest_theme_renders(self):
        slides_data = [
            SlideData(title="Forest Test", content=["A", "B"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_forest")
        paths = create_slide_images(slides_data, images_dir, theme=SlideTheme.FOREST)
        assert len(paths) == 1
        assert os.path.getsize(paths[0]) > 0

    def test_royal_theme_renders(self):
        slides_data = [
            SlideData(title="Royal Test", content=["C", "D"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_royal")
        paths = create_slide_images(slides_data, images_dir, theme=SlideTheme.ROYAL)
        assert len(paths) == 1

    def test_tech_theme_renders(self):
        slides_data = [
            SlideData(title="Tech Test", content=["E"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_tech")
        paths = create_slide_images(slides_data, images_dir, theme=SlideTheme.TECH)
        assert len(paths) == 1

    def test_new_themes_pptx(self):
        """New themes should produce valid PPTX files."""
        slides_data = [
            SlideData(title="T", content=["X"], layout=SlideLayout.CONTENT),
        ]
        for theme in [SlideTheme.FOREST, SlideTheme.ROYAL, SlideTheme.TECH]:
            path = os.path.join(OUTPUT_DIR, f"new_{theme.value}.pptx")
            create_pptx_file(slides_data, path, theme=theme)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0

    def test_all_themes_count(self):
        """Should now have 8 themes total."""
        assert len(SlideTheme) == 8

    def test_new_themes_all_layouts(self):
        """New themes should render all layout types correctly."""
        slides_data = [
            SlideData(title="Title", content=["Sub"], layout=SlideLayout.TITLE),
            SlideData(title="Content", content=["A"], layout=SlideLayout.CONTENT),
            SlideData(title="Section", content=[], layout=SlideLayout.SECTION),
            SlideData(title="TwoCol", content=["L", "R"], layout=SlideLayout.TWO_COLUMN),
        ]
        for theme in [SlideTheme.FOREST, SlideTheme.ROYAL, SlideTheme.TECH]:
            images_dir = os.path.join(OUTPUT_DIR, f"images_all_{theme.value}")
            paths = create_slide_images(slides_data, images_dir, theme=theme)
            assert len(paths) == 4


class TestPPTXBulletFormatting:
    """Tests for accent-colored PPTX bullets (v8)."""

    def test_format_pptx_bullet_does_not_raise(self):
        """Formatting a PPTX paragraph bullet should not raise."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        if len(slide.placeholders) > 1:
            ph = slide.placeholders[1]
            if ph.has_text_frame:
                ph.text_frame.text = "Test bullet"
                colors = THEMES[SlideTheme.OCEAN]
                _format_pptx_bullet(ph.text_frame.paragraphs[0], colors)

    def test_pptx_content_has_bullets(self):
        """PPTX content slide should have formatted bullets."""
        slides_data = [
            SlideData(title="Bullets", content=["Point 1", "Point 2", "Point 3"],
                      layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "pptx_bullets.pptx")
        create_pptx_file(slides_data, path, theme=SlideTheme.OCEAN)
        assert os.path.exists(path)
        prs = Presentation(path)
        assert len(prs.slides) == 1


class TestPPTXSectionEnhanced:
    """Tests for enhanced PPTX section slide with shapes (v8)."""

    def test_pptx_section_has_shapes(self):
        """PPTX section slide should have accent bar and underline shapes."""
        slides_data = [
            SlideData(title="Section Test", content=[], layout=SlideLayout.SECTION),
        ]
        path = os.path.join(OUTPUT_DIR, "pptx_section_v8.pptx")
        create_pptx_file(slides_data, path)
        prs = Presentation(path)
        slide = prs.slides[0]
        # Should have shapes beyond the default (title + accent bar + underline)
        assert len(slide.shapes) >= 2

    def test_pptx_section_all_themes(self):
        """PPTX section slides should work across all themes."""
        slides_data = [
            SlideData(title="Sec", content=[], layout=SlideLayout.SECTION),
        ]
        for theme in SlideTheme:
            path = os.path.join(OUTPUT_DIR, f"pptx_sec_{theme.value}.pptx")
            create_pptx_file(slides_data, path, theme=theme)
            assert os.path.exists(path)


class TestPPTXEntranceAnimations:
    """Tests for PPTX bullet-by-bullet entrance animations (v9)."""

    def test_animation_does_not_raise(self):
        """Adding entrance animations to a slide should not raise."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        if len(slide.placeholders) > 1:
            ph = slide.placeholders[1]
            if ph.has_text_frame:
                ph.text_frame.text = "First"
                ph.text_frame.add_paragraph().text = "Second"
                _add_pptx_entrance_animations(slide, ph.shape_id, 2)

    def test_animation_zero_paragraphs(self):
        """Zero paragraphs should be a no-op."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        _add_pptx_entrance_animations(slide, 99, 0)  # should not raise

    def test_pptx_with_animations_enabled(self):
        """PPTX with animations enabled should produce a valid file."""
        slides_data = [
            SlideData(title="Animated", content=["A", "B", "C"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "animated.pptx")
        create_pptx_file(slides_data, path, enable_animations=True)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

    def test_pptx_with_animations_disabled(self):
        """PPTX with animations disabled should also produce a valid file."""
        slides_data = [
            SlideData(title="No Anim", content=["X", "Y"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "no_anim.pptx")
        create_pptx_file(slides_data, path, enable_animations=False)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

    def test_pptx_animations_all_themes(self):
        """Animations should work across all themes."""
        slides_data = [
            SlideData(title="Theme Anim", content=["P1", "P2"], layout=SlideLayout.CONTENT),
        ]
        for theme in SlideTheme:
            path = os.path.join(OUTPUT_DIR, f"anim_{theme.value}.pptx")
            create_pptx_file(slides_data, path, theme=theme, enable_animations=True)
            assert os.path.exists(path)


class TestSRTSubtitles:
    """Tests for SRT subtitle generation (v9)."""

    def test_format_srt_timestamp(self):
        """SRT timestamp formatting should produce correct format."""
        assert _format_srt_timestamp(0.0) == "00:00:00,000"
        assert _format_srt_timestamp(1.5) == "00:00:01,500"
        assert _format_srt_timestamp(65.25) == "00:01:05,250"
        assert _format_srt_timestamp(3661.0) == "01:01:01,000"

    def test_generate_srt_basic(self):
        """SRT generation with scripts and durations should produce valid file."""
        scripts = ["Hello world", "Second slide", "Conclusion"]
        durations = [5.0, 8.0, 4.0]
        srt_path = os.path.join(OUTPUT_DIR, "test.srt")
        result = generate_srt_subtitles(scripts, durations, srt_path)
        assert result == srt_path
        assert os.path.exists(srt_path)
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Hello world" in content
        assert "Second slide" in content
        assert "00:00:00,000" in content  # First subtitle starts at 0

    def test_generate_srt_empty_scripts(self):
        """Empty scripts should skip entries but not crash."""
        scripts = ["Hello", "", "End"]
        durations = [3.0, 2.0, 4.0]
        srt_path = os.path.join(OUTPUT_DIR, "sparse.srt")
        result = generate_srt_subtitles(scripts, durations, srt_path)
        assert result == srt_path
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Hello" in content
        assert "End" in content
        # Should have 2 entries (empty script skipped)
        assert content.count("-->") == 2

    def test_generate_srt_no_scripts(self):
        """No scripts should return None."""
        assert generate_srt_subtitles([], [], os.path.join(OUTPUT_DIR, "empty.srt")) is None

    def test_generate_srt_cjk(self):
        """SRT should handle CJK text correctly."""
        scripts = ["\u4eba\u5de5\u667a\u80fd\u6982\u8ff0", "\u673a\u5668\u5b66\u4e60\u5e94\u7528"]
        durations = [5.0, 5.0]
        srt_path = os.path.join(OUTPUT_DIR, "cjk.srt")
        result = generate_srt_subtitles(scripts, durations, srt_path)
        assert result == srt_path
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "\u4eba\u5de5\u667a\u80fd" in content


class TestConfigurableTransitions:
    """Tests for configurable transition duration (v9)."""

    def test_config_default_animation(self):
        config = PresentationConfig()
        assert config.enable_animations is True
        assert config.transition_duration_ms == 700

    def test_config_custom_animation(self):
        config = PresentationConfig(enable_animations=False, transition_duration_ms=1200)
        assert config.enable_animations is False
        assert config.transition_duration_ms == 1200

    def test_pptx_custom_transition_duration(self):
        """PPTX with custom transition duration should produce valid file."""
        slides_data = [
            SlideData(title="Slow Fade", content=["A"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "slow_transition.pptx")
        create_pptx_file(slides_data, path, transition_duration_ms=1500)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0


class TestTransitionPhrasesComplete:
    """Tests for complete transition phrases in all 7 languages (v9)."""

    def test_all_languages_have_phrases(self):
        """Every Language enum value should have transition phrases."""
        for lang in Language:
            assert lang in _TRANSITION_PHRASES, f"Missing phrases for {lang}"
            assert len(_TRANSITION_PHRASES[lang]) >= 3, f"Too few phrases for {lang}"

    def test_korean_phrases(self):
        assert Language.KOREAN in _TRANSITION_PHRASES
        assert len(_TRANSITION_PHRASES[Language.KOREAN]) >= 5

    def test_french_phrases(self):
        assert Language.FRENCH in _TRANSITION_PHRASES
        assert len(_TRANSITION_PHRASES[Language.FRENCH]) >= 5

    def test_german_phrases(self):
        assert Language.GERMAN in _TRANSITION_PHRASES
        assert len(_TRANSITION_PHRASES[Language.GERMAN]) >= 5

    def test_spanish_phrases(self):
        assert Language.SPANISH in _TRANSITION_PHRASES
        assert len(_TRANSITION_PHRASES[Language.SPANISH]) >= 5

    def test_speaker_notes_korean(self):
        """Korean speaker notes should use Korean phrases."""
        notes = _build_speaker_notes("AI \uac1c\uc694", ["\ub370\uc774\ud130"], 0, 5, Language.KOREAN)
        assert len(notes) > 0

    def test_speaker_notes_french(self):
        """French speaker notes should use French phrases."""
        notes = _build_speaker_notes("Introduction", ["Donn\u00e9es"], 1, 5, Language.FRENCH)
        assert len(notes) > 0


class TestContentValidation:
    """Tests for content validation warnings (v9)."""

    def test_validate_empty_slides(self):
        """Empty slide list should return a warning."""
        warnings = validate_content([])
        assert len(warnings) == 1

    def test_validate_duplicate_titles(self):
        """Duplicate titles should trigger a warning."""
        slides = [
            SlideData(title="Introduction", content=["A"], layout=SlideLayout.CONTENT),
            SlideData(title="Introduction", content=["B"], layout=SlideLayout.CONTENT),
        ]
        warnings = validate_content(slides)
        assert any("Duplicate title" in w for w in warnings)

    def test_validate_empty_content(self):
        """Content slides with no bullets should trigger a warning."""
        slides = [
            SlideData(title="Empty", content=[], layout=SlideLayout.CONTENT),
        ]
        warnings = validate_content(slides)
        assert any("no content" in w for w in warnings)

    def test_validate_too_many_bullets(self):
        """Slides with >8 bullets should trigger a warning."""
        slides = [
            SlideData(title="Dense", content=[f"Point {i}" for i in range(10)],
                      layout=SlideLayout.CONTENT),
        ]
        warnings = validate_content(slides)
        assert any("10 bullets" in w for w in warnings)

    def test_validate_missing_notes(self):
        """Slides without speaker notes should trigger a warning."""
        slides = [
            SlideData(title="No Notes", content=["A"], speaker_notes="",
                      layout=SlideLayout.CONTENT),
        ]
        warnings = validate_content(slides)
        assert any("missing speaker notes" in w for w in warnings)

    def test_validate_long_bullet(self):
        """Very long bullet points should trigger a warning."""
        long_point = "X" * 150
        slides = [
            SlideData(title="Long", content=[long_point], speaker_notes="notes",
                      layout=SlideLayout.CONTENT),
        ]
        warnings = validate_content(slides)
        assert any("too long" in w for w in warnings)

    def test_validate_good_content(self):
        """Well-structured slides should have minimal warnings."""
        slides = [
            SlideData(title="Title", content=["Sub"], speaker_notes="Welcome",
                      layout=SlideLayout.TITLE),
            SlideData(title="Content", content=["A", "B", "C"], speaker_notes="Points",
                      layout=SlideLayout.CONTENT),
            SlideData(title="Summary", content=["Key point"], speaker_notes="Wrap up",
                      layout=SlideLayout.CONTENT),
        ]
        warnings = validate_content(slides)
        # Title slide has empty content but that's ok (not CONTENT layout)
        assert not any("no content" in w for w in warnings)

    def test_validate_section_no_content_ok(self):
        """Section slides should not warn about missing content."""
        slides = [
            SlideData(title="Section", content=[], speaker_notes="Divider",
                      layout=SlideLayout.SECTION),
        ]
        warnings = validate_content(slides)
        assert not any("no content" in w for w in warnings)


class TestTransitionDurationFix:
    """Tests for fixed transition duration (v10 - was ignored before)."""

    def test_transition_uses_dur_attribute(self):
        """Transition element should have dur attribute matching duration_ms."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        _add_pptx_slide_transition(slide, duration_ms=1500)
        # Check the transition XML has dur="1500"
        from lxml import etree
        from pptx.oxml.ns import qn
        trans = slide._element.findall(qn("p:transition"))
        assert len(trans) == 1
        assert trans[0].get("dur") == "1500"

    def test_transition_default_duration(self):
        """Default transition should use 700ms."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        _add_pptx_slide_transition(slide)
        from lxml import etree
        from pptx.oxml.ns import qn
        trans = slide._element.findall(qn("p:transition"))
        assert trans[0].get("dur") == "700"

    def test_transition_no_spd_attribute(self):
        """Transition should use dur, not the deprecated spd attribute."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        _add_pptx_slide_transition(slide, duration_ms=1000)
        from pptx.oxml.ns import qn
        trans = slide._element.findall(qn("p:transition"))
        assert trans[0].get("spd") is None  # deprecated attribute should not be present


class TestSpeakerNotesEnhancedV10:
    """Tests for improved speaker notes quality (v10)."""

    def test_closing_phrases_all_languages(self):
        """All 7 languages should have closing phrases."""
        for lang in Language:
            assert lang in _CLOSING_PHRASES, f"Missing closing phrase for {lang}"
            assert len(_CLOSING_PHRASES[lang]) > 10  # minimum length

    def test_emphasis_connectors_all_languages(self):
        """All 7 languages should have emphasis connectors."""
        for lang in Language:
            assert lang in _EMPHASIS_CONNECTORS, f"Missing connectors for {lang}"
            assert len(_EMPHASIS_CONNECTORS[lang]) >= 3

    def test_notes_use_connectors_for_middle_slides(self):
        """Middle slides should include emphasis connectors in notes."""
        notes = _build_speaker_notes("Test Topic", ["Point A", "Point B"], 2, 5, Language.ENGLISH)
        # Should contain one of the English connectors
        connectors = _EMPHASIS_CONNECTORS[Language.ENGLISH]
        assert any(c in notes for c in connectors)

    def test_notes_use_closing_for_last_slide(self):
        """Last slide should use closing phrase."""
        notes = _build_speaker_notes("Summary", ["Key point"], 4, 5, Language.FRENCH)
        assert _CLOSING_PHRASES[Language.FRENCH][:15] in notes

    def test_notes_longer_than_before(self):
        """Notes should allow up to 500 chars (up from 400)."""
        long_content = [f"This is a fairly long bullet point number {i}" for i in range(5)]
        notes = _build_speaker_notes("Detailed Topic", long_content, 1, 5, Language.ENGLISH)
        # Notes should be allowed up to 500 chars
        assert len(notes) <= 500

    def test_notes_korean_closing(self):
        """Korean closing phrase should be used for last slide."""
        notes = _build_speaker_notes("요약", ["핵심 내용"], 4, 5, Language.KOREAN)
        assert _CLOSING_PHRASES[Language.KOREAN][:5] in notes

    def test_notes_german_connector(self):
        """German middle slide should use German connector."""
        notes = _build_speaker_notes("Thema", ["Punkt A"], 2, 5, Language.GERMAN)
        connectors = _EMPHASIS_CONNECTORS[Language.GERMAN]
        assert any(c in notes for c in connectors)

    def test_notes_spanish_closing(self):
        """Spanish closing phrase should be used for last slide."""
        notes = _build_speaker_notes("Resumen", ["Punto clave"], 4, 5, Language.SPANISH)
        assert _CLOSING_PHRASES[Language.SPANISH][:10] in notes


class TestPPTXTransitionDurationIntegration:
    """Integration tests for transition duration flowing through PPTX creation."""

    def test_pptx_file_with_fast_transitions(self):
        """PPTX with fast transitions (200ms) should be valid."""
        slides_data = [
            SlideData(title="Fast", content=["Quick transitions"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "fast_trans.pptx")
        create_pptx_file(slides_data, path, transition_duration_ms=200)
        assert os.path.exists(path)

    def test_pptx_file_with_slow_transitions(self):
        """PPTX with slow transitions (2000ms) should be valid."""
        slides_data = [
            SlideData(title="Slow", content=["Slow transitions"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "slow_trans.pptx")
        create_pptx_file(slides_data, path, transition_duration_ms=2000)
        assert os.path.exists(path)


class TestPPTXTransitionTypes:
    """Tests for multiple PPTX transition types (v11)."""

    def test_transition_types_list(self):
        """Should have 6 supported transition types."""
        assert len(PPTX_TRANSITION_TYPES) == 6
        assert "fade" in PPTX_TRANSITION_TYPES
        assert "push" in PPTX_TRANSITION_TYPES
        assert "wipe" in PPTX_TRANSITION_TYPES
        assert "cover" in PPTX_TRANSITION_TYPES
        assert "split" in PPTX_TRANSITION_TYPES
        assert "dissolve" in PPTX_TRANSITION_TYPES

    def test_all_transition_types_xml(self):
        """Each transition type should produce the correct OpenXML element."""
        from pptx.oxml.ns import qn as _qn
        for ttype in PPTX_TRANSITION_TYPES:
            prs = Presentation()
            prs.slide_width = Inches(13.333)
            prs.slide_height = Inches(7.5)
            slide = prs.slides.add_slide(prs.slide_layouts[0])
            _add_pptx_slide_transition(slide, duration_ms=500, transition_type=ttype)
            trans = slide._element.findall(_qn("p:transition"))
            assert len(trans) == 1, f"No transition for type {ttype}"
            # Should have exactly one child element for the transition type
            children = list(trans[0])
            assert len(children) == 1, f"Expected 1 child for {ttype}, got {len(children)}"

    def test_unknown_type_falls_back_to_fade(self):
        """Unknown transition type should fall back to fade."""
        from pptx.oxml.ns import qn as _qn
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        _add_pptx_slide_transition(slide, transition_type="unknown_type")
        trans = slide._element.findall(_qn("p:transition"))
        assert len(trans) == 1
        child = list(trans[0])[0]
        assert "fade" in child.tag

    def test_pptx_with_push_transition(self):
        """PPTX with push transition should produce valid file."""
        slides_data = [
            SlideData(title="Push", content=["A", "B"], layout=SlideLayout.CONTENT),
            SlideData(title="Slide 2", content=["C"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "push_transition.pptx")
        create_pptx_file(slides_data, path, transition_type="push")
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

    def test_pptx_with_wipe_transition(self):
        """PPTX with wipe transition should produce valid file."""
        slides_data = [
            SlideData(title="Wipe", content=["X"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "wipe_transition.pptx")
        create_pptx_file(slides_data, path, transition_type="wipe")
        assert os.path.exists(path)

    def test_config_transition_type_default(self):
        """PresentationConfig should default to 'fade' transition."""
        config = PresentationConfig()
        assert config.transition_type == "fade"

    def test_config_transition_type_custom(self):
        """PresentationConfig should accept custom transition type."""
        config = PresentationConfig(transition_type="dissolve")
        assert config.transition_type == "dissolve"


class TestPDFMetadata:
    """Tests for PDF metadata (title, author) in v11."""

    def test_pdf_with_metadata(self):
        """PDF with title and author should be valid."""
        slides_data = [
            SlideData(title="Meta Test", content=["A"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_meta")
        image_paths = create_slide_images(slides_data, images_dir)
        pdf_path = os.path.join(OUTPUT_DIR, "meta.pdf")
        result = create_pdf_from_images(image_paths, pdf_path, title="My Presentation", author="John")
        assert result == pdf_path
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0

    def test_pdf_without_metadata(self):
        """PDF without metadata should still work."""
        slides_data = [
            SlideData(title="No Meta", content=["B"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_no_meta")
        image_paths = create_slide_images(slides_data, images_dir)
        pdf_path = os.path.join(OUTPUT_DIR, "no_meta.pdf")
        result = create_pdf_from_images(image_paths, pdf_path)
        assert result == pdf_path
        assert os.path.exists(pdf_path)

    def test_pdf_title_only(self):
        """PDF with only title (no author) should work."""
        slides_data = [
            SlideData(title="Title Only", content=["C"], layout=SlideLayout.CONTENT),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_title_only")
        image_paths = create_slide_images(slides_data, images_dir)
        pdf_path = os.path.join(OUTPUT_DIR, "title_only.pdf")
        result = create_pdf_from_images(image_paths, pdf_path, title="Just Title")
        assert result == pdf_path
        assert os.path.exists(pdf_path)


class TestSummaryTitlesModuleLevel:
    """Tests for _SUMMARY_TITLES at module level (v11 cleanup)."""

    def test_summary_titles_all_languages(self):
        """All 7 languages should have summary titles."""
        for lang in Language:
            assert lang in _SUMMARY_TITLES, f"Missing summary title for {lang}"
            assert len(_SUMMARY_TITLES[lang]) > 0

    def test_summary_titles_english(self):
        assert _SUMMARY_TITLES[Language.ENGLISH] == "Key Takeaways"

    def test_summary_titles_chinese(self):
        assert _SUMMARY_TITLES[Language.CHINESE] == "\u6838\u5fc3\u8981\u70b9"

    def test_mock_uses_module_level_summary(self):
        """Mock generation should use the module-level _SUMMARY_TITLES dict."""
        text = "AI is great. ML is powerful. DL is deep. NLP reads text. CV sees images. " * 10
        for lang in [Language.ENGLISH, Language.CHINESE, Language.JAPANESE]:
            slides = mock_generate_content(text, num_slides=5, language=lang)
            last = slides[-1]
            assert last.title == _SUMMARY_TITLES[lang]


class TestPresentationStatistics:
    """Tests for presentation statistics computation logic (v11)."""

    def test_word_count_calculation(self):
        """Verify word counting logic for slides."""
        slides = [
            SlideData(title="T1", content=["Word1 Word2", "Word3"], speaker_notes="Note word"),
            SlideData(title="T2", content=["A B C"], speaker_notes="D E"),
        ]
        total_words = sum(
            len((" ".join(s.content) + " " + s.speaker_notes).split())
            for s in slides
        )
        # Slide 1: "Word1 Word2 Word3" + "Note word" = 5 words
        # Slide 2: "A B C" + "D E" = 5 words
        assert total_words == 10

    def test_bullet_count(self):
        """Total bullet count should sum all content items."""
        slides = [
            SlideData(title="T1", content=["A", "B", "C"], speaker_notes=""),
            SlideData(title="T2", content=["D"], speaker_notes=""),
        ]
        total_bullets = sum(len(s.content) for s in slides)
        assert total_bullets == 4

    def test_duration_estimate(self):
        """Duration estimate at 150 wpm should be reasonable."""
        # 300 words / 150 wpm = 2 minutes
        total_words = 300
        est_duration_min = max(1, round(total_words / 150))
        assert est_duration_min == 2

    def test_layout_distribution(self):
        """Layout distribution counting should work."""
        slides = [
            SlideData(title="T", content=[], layout=SlideLayout.TITLE),
            SlideData(title="C1", content=["A"], layout=SlideLayout.CONTENT),
            SlideData(title="C2", content=["B"], layout=SlideLayout.CONTENT),
            SlideData(title="S", content=[], layout=SlideLayout.SECTION),
        ]
        layout_counts = {}
        for s in slides:
            layout_counts[s.layout.value] = layout_counts.get(s.layout.value, 0) + 1
        assert layout_counts["title"] == 1
        assert layout_counts["content"] == 2
        assert layout_counts["section"] == 1


class TestProjectSerialize:
    """Tests for JSON project export/import (v12)."""

    def test_serialize_basic(self):
        """Serialize slides to a project dict."""
        slides = [
            SlideData(title="Title", content=["Sub"], layout=SlideLayout.TITLE),
            SlideData(title="Content", content=["A", "B"], speaker_notes="Notes",
                      layout=SlideLayout.CONTENT),
        ]
        proj = serialize_project(slides, language="en", theme="professional")
        assert proj["version"] == "15.0"
        assert len(proj["slides"]) == 2
        assert proj["settings"]["language"] == "en"
        assert proj["settings"]["theme"] == "professional"

    def test_serialize_with_extra_kwargs(self):
        """Extra settings should be preserved."""
        slides = [SlideData(title="T", content=["A"])]
        proj = serialize_project(slides, language="zh", theme="dark",
                                 footer_company="ACME", footer_author="Jane")
        assert proj["settings"]["footer_company"] == "ACME"
        assert proj["settings"]["footer_author"] == "Jane"

    def test_deserialize_basic(self):
        """Deserialize project dict back to slides."""
        data = {
            "version": "12.0",
            "settings": {"language": "en", "theme": "ocean"},
            "slides": [
                {"title": "S1", "content": ["A"], "layout": "content"},
                {"title": "S2", "content": ["B", "C"], "layout": "title"},
            ],
        }
        slides, settings = deserialize_project(data)
        assert len(slides) == 2
        assert slides[0].title == "S1"
        assert slides[1].layout == SlideLayout.TITLE
        assert settings["theme"] == "ocean"

    def test_roundtrip(self):
        """Serialize then deserialize should preserve data."""
        original = [
            SlideData(title="Intro", content=["Welcome"], speaker_notes="Hello",
                      image_prompt="bg", layout=SlideLayout.TITLE),
            SlideData(title="Body", content=["X", "Y"], speaker_notes="Main",
                      layout=SlideLayout.CONTENT),
        ]
        proj = serialize_project(original, language="fr", theme="sunset")
        slides, settings = deserialize_project(proj)
        assert len(slides) == len(original)
        for orig, loaded in zip(original, slides):
            assert orig.title == loaded.title
            assert orig.content == loaded.content
            assert orig.speaker_notes == loaded.speaker_notes
            assert orig.layout == loaded.layout

    def test_deserialize_empty(self):
        """Empty project should return empty lists."""
        slides, settings = deserialize_project({})
        assert slides == []
        assert settings == {}

    def test_serialize_json_compatible(self):
        """Output should be JSON-serializable."""
        import json
        slides = [SlideData(title="CJK \u4eba\u5de5\u667a\u80fd", content=["\u673a\u5668\u5b66\u4e60"])]
        proj = serialize_project(slides, language="zh")
        json_str = json.dumps(proj, ensure_ascii=False)
        assert "\u4eba\u5de5\u667a\u80fd" in json_str
        loaded = json.loads(json_str)
        assert loaded["slides"][0]["title"] == "CJK \u4eba\u5de5\u667a\u80fd"


class TestTwoColumnOverflow:
    """Tests for two-column overflow protection (v12)."""

    def test_many_items_two_column_renders(self):
        """Two-column slide with many items should render without error."""
        slides_data = [
            SlideData(
                title="Dense Two Column",
                content=[f"Long bullet point number {i} with lots of text in it" for i in range(20)],
                layout=SlideLayout.TWO_COLUMN,
            ),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_2col_overflow")
        image_paths = create_slide_images(slides_data, images_dir)
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_long_text_two_column_renders(self):
        """Two-column with very long bullet text should render with truncation."""
        long_text = "This is an extremely long bullet point that goes on and on " * 5
        slides_data = [
            SlideData(
                title="Long Text Columns",
                content=[long_text, long_text, "Short", "Also short",
                         long_text, long_text],
                layout=SlideLayout.TWO_COLUMN,
            ),
        ]
        images_dir = os.path.join(OUTPUT_DIR, "images_2col_long")
        image_paths = create_slide_images(slides_data, images_dir)
        assert len(image_paths) == 1
        assert os.path.getsize(image_paths[0]) > 0

    def test_two_column_all_themes_overflow(self):
        """Overflow protection should work across all themes."""
        slides_data = [
            SlideData(
                title="Theme Overflow",
                content=[f"Item {i}" for i in range(16)],
                layout=SlideLayout.TWO_COLUMN,
            ),
        ]
        for theme in [SlideTheme.DARK, SlideTheme.TECH, SlideTheme.FOREST]:
            images_dir = os.path.join(OUTPUT_DIR, f"images_2col_{theme.value}")
            image_paths = create_slide_images(slides_data, images_dir, theme=theme)
            assert len(image_paths) == 1


class TestSlideSearchFilter:
    """Tests for slide search/filter logic (v12)."""

    def test_filter_by_title(self):
        """Filtering slides by title keyword should return matching indices."""
        slides = [
            SlideData(title="Introduction", content=["A"]),
            SlideData(title="Methods", content=["B"]),
            SlideData(title="Results and Analysis", content=["C"]),
        ]
        q = "method"
        indices = [i for i, s in enumerate(slides)
                   if q in s.title.lower() or any(q in b.lower() for b in s.content)]
        assert indices == [1]

    def test_filter_by_content(self):
        """Filtering by content text should match."""
        slides = [
            SlideData(title="T1", content=["Machine learning is powerful"]),
            SlideData(title="T2", content=["Deep learning intro"]),
        ]
        q = "machine"
        indices = [i for i, s in enumerate(slides)
                   if q in s.title.lower() or any(q in b.lower() for b in s.content)]
        assert indices == [0]

    def test_filter_empty_query_shows_all(self):
        """Empty search query should show all slides."""
        slides = [SlideData(title="A", content=[]), SlideData(title="B", content=[])]
        q = ""
        if q.strip():
            indices = [i for i, s in enumerate(slides) if q in s.title.lower()]
        else:
            indices = list(range(len(slides)))
        assert len(indices) == 2

    def test_filter_no_match(self):
        """Non-matching query should return empty."""
        slides = [SlideData(title="Hello", content=["World"])]
        q = "zzzzz"
        indices = [i for i, s in enumerate(slides)
                   if q in s.title.lower() or any(q in b.lower() for b in s.content)]
        assert indices == []


class TestPresenterNotesExport:
    """Tests for presenter notes TXT export (v12)."""

    def test_notes_export_format(self):
        """Notes export should produce correct format."""
        slides = [
            SlideData(title="Slide 1", content=["A"], speaker_notes="Welcome everyone"),
            SlideData(title="Slide 2", content=["B"], speaker_notes=""),
        ]
        notes_lines = []
        for idx, s in enumerate(slides):
            notes_lines.append(f"--- Slide {idx + 1}: {s.title} ---")
            notes_lines.append(s.speaker_notes if s.speaker_notes else "(no notes)")
            notes_lines.append("")
        notes_text = "\n".join(notes_lines)
        assert "--- Slide 1: Slide 1 ---" in notes_text
        assert "Welcome everyone" in notes_text
        assert "(no notes)" in notes_text

    def test_notes_export_cjk(self):
        """Notes export should handle CJK text."""
        slides = [
            SlideData(title="\u4eba\u5de5\u667a\u80fd", content=[],
                      speaker_notes="\u6b22\u8fce\u5927\u5bb6"),
        ]
        notes_lines = []
        for idx, s in enumerate(slides):
            notes_lines.append(f"--- Slide {idx + 1}: {s.title} ---")
            notes_lines.append(s.speaker_notes if s.speaker_notes else "(no notes)")
            notes_lines.append("")
        notes_text = "\n".join(notes_lines)
        assert "\u6b22\u8fce\u5927\u5bb6" in notes_text


class TestPPTXTwoColumnDualBoxes:
    """Tests for PPTX two-column with dual text boxes (v13)."""

    def test_two_column_pptx_has_divider(self):
        """Two-column PPTX should have a divider shape."""
        slides_data = [
            SlideData(title="Compare", content=["Left A", "Left B", "Right C", "Right D"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "two_col_dual.pptx")
        create_pptx_file(slides_data, path)
        prs = Presentation(path)
        slide = prs.slides[0]
        # Should have shapes: title box, divider, left box, right box = at least 4
        assert len(slide.shapes) >= 4

    def test_two_column_pptx_content_split(self):
        """Content should be split between two text boxes."""
        slides_data = [
            SlideData(title="Split", content=["A", "B", "C", "D"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "two_col_split.pptx")
        create_pptx_file(slides_data, path)
        prs = Presentation(path)
        slide = prs.slides[0]
        # Count text boxes with actual content
        text_shapes = [s for s in slide.shapes if s.has_text_frame and s.text_frame.text.strip()]
        # Should have title + left + right = 3 text-containing shapes
        assert len(text_shapes) >= 3

    def test_two_column_pptx_single_item(self):
        """Single-item two-column should still render."""
        slides_data = [
            SlideData(title="Solo", content=["Only one item"], layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "two_col_solo.pptx")
        create_pptx_file(slides_data, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

    def test_two_column_pptx_many_items(self):
        """Many items in two-column should not crash."""
        slides_data = [
            SlideData(title="Many", content=[f"Item {i}" for i in range(12)],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "two_col_many.pptx")
        create_pptx_file(slides_data, path)
        assert os.path.exists(path)

    def test_two_column_all_themes(self):
        """Two-column dual boxes should work across themes."""
        slides_data = [
            SlideData(title="Theme Test", content=["A", "B", "C", "D"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        for theme in [SlideTheme.DARK, SlideTheme.OCEAN, SlideTheme.TECH]:
            path = os.path.join(OUTPUT_DIR, f"two_col_{theme.value}.pptx")
            create_pptx_file(slides_data, path, theme=theme)
            assert os.path.exists(path)


class TestExtractJson:
    """Tests for _extract_json helper (v13)."""

    def test_plain_json(self):
        """Plain JSON string should parse directly."""
        data = _extract_json('{"slides": [{"title": "A"}]}')
        assert data["slides"][0]["title"] == "A"

    def test_json_in_code_fence(self):
        """JSON inside markdown code fence should be extracted."""
        text = 'Here is the result:\n```json\n{"slides": [{"title": "B"}]}\n```\nDone.'
        data = _extract_json(text)
        assert data["slides"][0]["title"] == "B"

    def test_json_in_plain_fence(self):
        """JSON inside ``` fence without json tag should work."""
        text = '```\n{"key": "value"}\n```'
        data = _extract_json(text)
        assert data["key"] == "value"

    def test_json_with_leading_text(self):
        """JSON preceded by non-JSON text should be extracted."""
        text = 'The response is: {"slides": [{"title": "C"}]}'
        data = _extract_json(text)
        assert data["slides"][0]["title"] == "C"

    def test_json_with_trailing_text(self):
        """JSON followed by non-JSON text should be extracted."""
        text = '{"answer": 42} hope this helps!'
        data = _extract_json(text)
        assert data["answer"] == 42

    def test_nested_json_extraction(self):
        """Nested JSON objects should parse correctly."""
        text = 'Output: {"outer": {"inner": [1, 2, 3]}} end'
        data = _extract_json(text)
        assert data["outer"]["inner"] == [1, 2, 3]

    def test_invalid_json_raises(self):
        """Completely invalid text should raise JSONDecodeError."""
        import json
        with pytest.raises(json.JSONDecodeError):
            _extract_json("This is not JSON at all")

    def test_empty_string_raises(self):
        """Empty string should raise JSONDecodeError."""
        import json
        with pytest.raises(json.JSONDecodeError):
            _extract_json("")


class TestSlideDurationOverride:
    """Tests for per-slide duration override (v13)."""

    def test_duration_override_default_none(self):
        """SlideData should default to None duration_override."""
        s = SlideData(title="T", content=["A"])
        assert s.duration_override is None

    def test_duration_override_set(self):
        """duration_override should be settable."""
        s = SlideData(title="T", content=["A"], duration_override=5.0)
        assert s.duration_override == 5.0

    def test_duration_override_to_dict(self):
        """to_dict should include duration_override when set."""
        s = SlideData(title="T", content=["A"], duration_override=10.0)
        d = s.to_dict()
        assert d["duration_override"] == 10.0

    def test_duration_override_to_dict_none(self):
        """to_dict should omit duration_override when None."""
        s = SlideData(title="T", content=["A"])
        d = s.to_dict()
        assert "duration_override" not in d

    def test_duration_override_from_dict(self):
        """from_dict should restore duration_override."""
        d = {"title": "T", "content": ["A"], "duration_override": 7.5}
        s = SlideData.from_dict(d)
        assert s.duration_override == 7.5

    def test_duration_override_from_dict_missing(self):
        """from_dict without duration_override should default to None."""
        d = {"title": "T", "content": ["A"]}
        s = SlideData.from_dict(d)
        assert s.duration_override is None

    def test_duration_override_roundtrip(self):
        """Serialize then deserialize should preserve duration."""
        original = SlideData(title="T", content=["A"], duration_override=15.0)
        d = original.to_dict()
        loaded = SlideData.from_dict(d)
        assert loaded.duration_override == original.duration_override

    def test_duration_override_project_roundtrip(self):
        """Project save/load should preserve duration_override."""
        slides = [
            SlideData(title="S1", content=["A"], duration_override=5.0),
            SlideData(title="S2", content=["B"]),
        ]
        proj = serialize_project(slides, language="en")
        loaded_slides, _ = deserialize_project(proj)
        assert loaded_slides[0].duration_override == 5.0
        assert loaded_slides[1].duration_override is None


class TestPPTXHeaderBar:
    """Tests for PPTX header bar shapes (v14)."""

    def test_header_bar_does_not_raise(self):
        """Adding a header bar to a slide should not raise."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        colors = THEMES[SlideTheme.PROFESSIONAL]
        _add_pptx_header_bar(slide, colors)

    def test_header_bar_adds_shapes(self):
        """Header bar should add header rectangle + accent line shapes."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        shapes_before = len(slide.shapes)
        colors = THEMES[SlideTheme.OCEAN]
        _add_pptx_header_bar(slide, colors)
        # Should have 2 additional shapes (header rect + accent line)
        assert len(slide.shapes) >= shapes_before + 2

    def test_content_slide_has_header_bar(self):
        """Content slides should include header bar shapes."""
        slides_data = [
            SlideData(title="Header Test", content=["A", "B"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "header_content.pptx")
        create_pptx_file(slides_data, path)
        prs = Presentation(path)
        slide = prs.slides[0]
        # Count non-textframe shapes (rectangles for header bar + accent line)
        rect_shapes = [s for s in slide.shapes if not s.has_text_frame or not s.text_frame.text.strip()]
        assert len(rect_shapes) >= 2

    def test_two_column_has_header_bar(self):
        """Two-column slides should include header bar shapes."""
        slides_data = [
            SlideData(title="Two Col Header", content=["L1", "L2", "R1", "R2"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "header_two_col.pptx")
        create_pptx_file(slides_data, path)
        prs = Presentation(path)
        slide = prs.slides[0]
        # Should have header bar, accent line, divider = at least 3 non-text shapes
        total_shapes = len(slide.shapes)
        assert total_shapes >= 6  # header + accent + title + divider + left + right

    def test_header_bar_all_themes(self):
        """Header bar should work across all themes."""
        slides_data = [
            SlideData(title="Theme Header", content=["X"], layout=SlideLayout.CONTENT),
        ]
        for theme in SlideTheme:
            path = os.path.join(OUTPUT_DIR, f"header_{theme.value}.pptx")
            create_pptx_file(slides_data, path, theme=theme)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0

    def test_content_slide_title_uses_title_color(self):
        """Content slide title text should use theme title color for readability on header bar."""
        slides_data = [
            SlideData(title="White Title", content=["Point"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "title_color.pptx")
        create_pptx_file(slides_data, path, theme=SlideTheme.PROFESSIONAL)
        prs = Presentation(path)
        slide = prs.slides[0]
        # Title should be white (255,255,255) for PROFESSIONAL theme
        if slide.shapes.title:
            for p in slide.shapes.title.text_frame.paragraphs:
                for run in p.runs:
                    assert run.font.color.rgb == RGBColor(255, 255, 255)


class TestTwoColumnAnimationFallback:
    """Tests for two-column animation fallback to text boxes (v14)."""

    def test_two_column_animation_produces_timing(self):
        """Two-column slides with animations should have p:timing XML."""
        from pptx.oxml.ns import qn as _qn
        slides_data = [
            SlideData(title="Anim Test", content=["A", "B", "C", "D"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "two_col_anim.pptx")
        create_pptx_file(slides_data, path, enable_animations=True)
        prs = Presentation(path)
        slide = prs.slides[0]
        timing = slide._element.findall(_qn("p:timing"))
        assert len(timing) >= 1

    def test_two_column_no_animation_when_disabled(self):
        """Two-column slides without animations should have no p:timing."""
        from pptx.oxml.ns import qn as _qn
        slides_data = [
            SlideData(title="No Anim", content=["A", "B", "C", "D"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "two_col_no_anim.pptx")
        create_pptx_file(slides_data, path, enable_animations=False)
        prs = Presentation(path)
        slide = prs.slides[0]
        timing = slide._element.findall(_qn("p:timing"))
        assert len(timing) == 0

    def test_content_slide_animation_still_works(self):
        """Content slides should still have animations via placeholder."""
        from pptx.oxml.ns import qn as _qn
        slides_data = [
            SlideData(title="Content Anim", content=["A", "B", "C"],
                      layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "content_anim.pptx")
        create_pptx_file(slides_data, path, enable_animations=True)
        prs = Presentation(path)
        slide = prs.slides[0]
        timing = slide._element.findall(_qn("p:timing"))
        assert len(timing) >= 1

    def test_mixed_layouts_animation(self):
        """Mixed layout deck with animations should not crash."""
        slides_data = [
            SlideData(title="Title", content=["Sub"], layout=SlideLayout.TITLE),
            SlideData(title="Content", content=["A", "B"], layout=SlideLayout.CONTENT),
            SlideData(title="Section", content=[], layout=SlideLayout.SECTION),
            SlideData(title="Two Col", content=["L1", "L2", "R1", "R2"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "mixed_anim.pptx")
        create_pptx_file(slides_data, path, enable_animations=True)
        assert os.path.exists(path)
        prs = Presentation(path)
        assert len(prs.slides) == 4


class TestProjectVersionString:
    """Tests for project serialization version (v14)."""

    def test_serialize_version_is_14(self):
        """Serialized project should have version 14.0."""
        slides = [SlideData(title="T", content=["A"])]
        proj = serialize_project(slides, language="en")
        assert proj["version"] == "15.0"

    def test_deserialize_ignores_version(self):
        """Deserialization should work regardless of version string."""
        data = {
            "version": "99.0",
            "settings": {"language": "en"},
            "slides": [{"title": "T", "content": ["X"]}],
        }
        slides, settings = deserialize_project(data)
        assert len(slides) == 1
        assert slides[0].title == "T"


class TestPPTXResponsiveFontSize:
    """Tests for responsive PPTX font sizing (v15)."""

    def test_few_items_uses_base_size(self):
        """Few items should use the base font size."""
        assert _compute_pptx_font_size(["Short", "Items"], base_size=18) == 18

    def test_many_items_shrinks_font(self):
        """Many items should trigger font shrinking."""
        items = [f"Item {i}" for i in range(10)]
        size = _compute_pptx_font_size(items, base_size=18)
        assert size < 18

    def test_long_text_shrinks_font(self):
        """Long text content should trigger font shrinking."""
        items = ["This is a very long bullet point " * 5 for _ in range(3)]
        size = _compute_pptx_font_size(items, base_size=18)
        assert size < 18

    def test_respects_min_size(self):
        """Font size should not shrink below min_size."""
        items = [f"Long item number {i} with extra text padding here" for i in range(20)]
        size = _compute_pptx_font_size(items, base_size=18, min_size=12)
        assert size >= 12

    def test_two_column_base_size(self):
        """Two-column base size (16) should be used correctly."""
        assert _compute_pptx_font_size(["A", "B"], base_size=16) == 16

    def test_content_slide_dense_renders(self):
        """Dense content slide should render with smaller fonts without error."""
        slides_data = [
            SlideData(title="Dense", content=[f"Point {i}: details here" for i in range(10)],
                      layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "dense_content.pptx")
        create_pptx_file(slides_data, path)
        assert os.path.exists(path)

    def test_two_column_dense_renders(self):
        """Dense two-column slide should render with responsive fonts."""
        slides_data = [
            SlideData(title="Dense Cols", content=[f"Item {i}" for i in range(12)],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "dense_two_col.pptx")
        create_pptx_file(slides_data, path)
        assert os.path.exists(path)


class TestPPTXGradientFill:
    """Tests for PPTX gradient header fills (v15)."""

    def test_gradient_header_renders(self):
        """Content slide with gradient header should render."""
        slides_data = [
            SlideData(title="Gradient", content=["A", "B"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "gradient_header.pptx")
        create_pptx_file(slides_data, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

    def test_gradient_header_has_grad_fill(self):
        """Header bar shape should contain a:gradFill element."""
        from pptx.oxml.ns import qn as _qn
        slides_data = [
            SlideData(title="GradCheck", content=["X"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "grad_check.pptx")
        create_pptx_file(slides_data, path)
        prs = Presentation(path)
        slide = prs.slides[0]
        # Search for gradFill element in any shape
        found_grad = False
        for shape in slide.shapes:
            sp_el = shape._element
            grad_fills = sp_el.findall(".//" + _qn("a:gradFill"))
            if grad_fills:
                found_grad = True
                break
        assert found_grad, "No gradient fill found in slide shapes"

    def test_gradient_all_themes(self):
        """Gradient headers should work with all themes."""
        slides_data = [
            SlideData(title="Theme Grad", content=["A"], layout=SlideLayout.CONTENT),
        ]
        for theme in SlideTheme:
            path = os.path.join(OUTPUT_DIR, f"grad_{theme.value}.pptx")
            create_pptx_file(slides_data, path, theme=theme)
            assert os.path.exists(path)

    def test_gradient_two_column(self):
        """Two-column slides should also have gradient headers."""
        from pptx.oxml.ns import qn as _qn
        slides_data = [
            SlideData(title="TwoCol Grad", content=["A", "B", "C", "D"],
                      layout=SlideLayout.TWO_COLUMN),
        ]
        path = os.path.join(OUTPUT_DIR, "grad_two_col.pptx")
        create_pptx_file(slides_data, path)
        prs = Presentation(path)
        slide = prs.slides[0]
        found_grad = False
        for shape in slide.shapes:
            grad_fills = shape._element.findall(".//" + _qn("a:gradFill"))
            if grad_fills:
                found_grad = True
                break
        assert found_grad


class TestPPTXProgressBar:
    """Tests for PPTX progress bar (v15)."""

    def test_progress_bar_does_not_raise(self):
        """Adding a progress bar should not raise."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        colors = THEMES[SlideTheme.PROFESSIONAL]
        _add_pptx_progress_bar(slide, 0, 5, colors)

    def test_progress_bar_adds_shapes(self):
        """Progress bar should add two rectangle shapes (bg + progress)."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        shapes_before = len(slide.shapes)
        colors = THEMES[SlideTheme.OCEAN]
        _add_pptx_progress_bar(slide, 2, 5, colors)
        assert len(slide.shapes) >= shapes_before + 2

    def test_progress_bar_skipped_single_slide(self):
        """Single-slide deck should not have progress bar."""
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        shapes_before = len(slide.shapes)
        colors = THEMES[SlideTheme.PROFESSIONAL]
        _add_pptx_progress_bar(slide, 0, 1, colors)
        assert len(slide.shapes) == shapes_before

    def test_progress_bar_in_full_deck(self):
        """Multi-slide deck should include progress bars."""
        slides_data = [
            SlideData(title="S1", content=["A"], layout=SlideLayout.CONTENT),
            SlideData(title="S2", content=["B"], layout=SlideLayout.CONTENT),
            SlideData(title="S3", content=["C"], layout=SlideLayout.CONTENT),
        ]
        path = os.path.join(OUTPUT_DIR, "progress_deck.pptx")
        create_pptx_file(slides_data, path)
        prs = Presentation(path)
        assert len(prs.slides) == 3
        # Each slide should have at least some shapes
        for slide in prs.slides:
            assert len(slide.shapes) >= 4  # header + accent + content + progress bars


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
