"""Tests for the content generator module."""
import pytest

from src.generator import generate_slides, mock_generate_content, _validate_slides, _assign_layouts
from src.models import SlideData, SlideLayout, Language


SAMPLE_TEXT = """Artificial Intelligence is transforming the world.
It is used in healthcare, finance, and transportation.
Machine learning is a subset of AI.
Deep learning is a subset of machine learning.
Neural networks are inspired by the human brain.
Natural language processing enables computers to understand text.
Computer vision allows machines to interpret images.
Reinforcement learning trains agents through rewards."""

SAMPLE_TEXT_CHINESE = """人工智能正在改变世界。
它在医疗、金融和交通领域广泛应用。
机器学习是人工智能的一个子集。
深度学习是机器学习的一个子集。
神经网络受到人类大脑的启发。"""


class TestMockGenerateContent:
    def test_generates_correct_count(self):
        slides = mock_generate_content(SAMPLE_TEXT, num_slides=3)
        assert len(slides) == 3

    def test_returns_slide_data_objects(self):
        slides = mock_generate_content(SAMPLE_TEXT, num_slides=3)
        for slide in slides:
            assert isinstance(slide, SlideData)

    def test_slides_have_required_fields(self):
        slides = mock_generate_content(SAMPLE_TEXT, num_slides=3)
        for slide in slides:
            assert slide.title
            assert slide.content
            assert slide.speaker_notes
            assert slide.image_prompt

    def test_single_slide(self):
        slides = mock_generate_content(SAMPLE_TEXT, num_slides=1)
        assert len(slides) == 1

    def test_many_slides(self):
        slides = mock_generate_content(SAMPLE_TEXT, num_slides=10)
        assert len(slides) == 10

    def test_empty_text_uses_placeholders(self):
        slides = mock_generate_content("", num_slides=3)
        assert len(slides) == 3

    def test_chinese_text(self):
        slides = mock_generate_content(SAMPLE_TEXT_CHINESE, num_slides=3, language=Language.CHINESE)
        assert len(slides) == 3

    def test_first_slide_has_title_layout(self):
        slides = mock_generate_content(SAMPLE_TEXT, num_slides=5)
        assert slides[0].layout == SlideLayout.TITLE

    def test_layouts_assigned(self):
        slides = mock_generate_content(SAMPLE_TEXT, num_slides=5)
        layouts = [s.layout for s in slides]
        assert SlideLayout.TITLE in layouts


class TestAssignLayouts:
    def test_first_slide_title(self):
        slides = [SlideData(title=f"Slide {i}") for i in range(5)]
        _assign_layouts(slides)
        assert slides[0].layout == SlideLayout.TITLE

    def test_section_dividers_for_long_presentations(self):
        slides = [SlideData(title=f"Slide {i}") for i in range(10)]
        _assign_layouts(slides)
        layouts = [s.layout for s in slides]
        assert SlideLayout.SECTION in layouts

    def test_two_column_for_many_bullets(self):
        slides = [
            SlideData(title="Title", content=["a"] * 2),
            SlideData(title="Many Bullets", content=["point"] * 7),
        ]
        _assign_layouts(slides)
        assert slides[1].layout == SlideLayout.TWO_COLUMN

    def test_empty_slides(self):
        _assign_layouts([])  # Should not raise


class TestGenerateSlides:
    def test_no_api_key_uses_mock(self):
        slides = generate_slides(SAMPLE_TEXT, num_slides=3)
        assert len(slides) == 3
        for slide in slides:
            assert isinstance(slide, SlideData)

    def test_with_language_parameter(self):
        slides = generate_slides(SAMPLE_TEXT, num_slides=3, language=Language.ENGLISH)
        assert len(slides) == 3

    def test_different_slide_counts(self):
        for n in [3, 5, 7]:
            slides = generate_slides(SAMPLE_TEXT, num_slides=n)
            assert len(slides) == n

    def test_custom_prompt_parameter(self):
        slides = generate_slides(SAMPLE_TEXT, num_slides=3, custom_prompt="Be concise")
        assert len(slides) == 3


class TestValidateSlides:
    def test_valid_slide_data(self):
        raw = [
            {"title": "Test", "content": ["Point 1", "Point 2"], "speaker_notes": "Notes", "image_prompt": "Image"},
        ]
        result = _validate_slides(raw, 1)
        assert len(result) == 1
        assert result[0].title == "Test"

    def test_content_as_string_converted_to_list(self):
        raw = [{"title": "Test", "content": "Single string"}]
        result = _validate_slides(raw, 1)
        assert result[0].content == ["Single string"]

    def test_short_title_replaced(self):
        raw = [{"title": "A"}]
        result = _validate_slides(raw, 1)
        assert result[0].title == "Slide 1"

    def test_non_dict_skipped(self):
        raw = ["not a dict", {"title": "Valid Slide"}]
        result = _validate_slides(raw, 2)
        assert len(result) == 1

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="No valid slides"):
            _validate_slides([], 1)

    def test_layout_parsed(self):
        raw = [{"title": "Test", "layout": "title"}]
        result = _validate_slides(raw, 1)
        assert result[0].layout == SlideLayout.TITLE

    def test_invalid_layout_defaults_to_content(self):
        raw = [{"title": "Test", "layout": "invalid_layout"}]
        result = _validate_slides(raw, 1)
        assert result[0].layout == SlideLayout.CONTENT


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
