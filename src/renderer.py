"""
Slide rendering module - generates PPTX, slide images, and PDF output.
Supports multiple visual themes, slide layouts, themed PPTX output,
AI background image compositing, CJK text wrapping, and text shadows.
"""
import os
import logging
import textwrap
from typing import List, Optional

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFont

from src.models import SlideData, SlideLayout, SlideTheme, Language, ThemeColors, THEMES
from src.config import (
    SLIDE_WIDTH, SLIDE_HEIGHT,
    TITLE_FONT_SIZE, CONTENT_FONT_SIZE, FOOTER_FONT_SIZE,
    TEXT_WRAP_WIDTH, BG_OVERLAY_OPACITY,
)

logger = logging.getLogger(__name__)

# Layout constants
MARGIN_X = 100
HEADER_HEIGHT = 200
CONTENT_START_Y = 280
LINE_SPACING = 75
BULLET_INDENT = 30

# Available pixel widths for text content
CONTENT_MAX_WIDTH = SLIDE_WIDTH - 2 * MARGIN_X       # ~1720px for full-width content
COLUMN_MAX_WIDTH = SLIDE_WIDTH // 2 - MARGIN_X - 40  # ~820px per column

# Text shadow settings
_SHADOW_OFFSET = 2
_SHADOW_COLOR = (0, 0, 0)

# CJK language set and font paths
_CJK_LANGUAGES = {Language.CHINESE, Language.JAPANESE, Language.KOREAN}

_CJK_FONT_PATHS = [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
    "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansSC-Regular.otf",
]

_CJK_BOLD_FONT_PATHS = [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansSC-Bold.otf",
]


# ---- CJK Detection & Text Wrapping ----

def _is_cjk_char(ch: str) -> bool:
    """Check if a character is CJK, Hiragana, Katakana, Hangul, or fullwidth."""
    cp = ord(ch)
    return (
        (0x4E00 <= cp <= 0x9FFF) or    # CJK Unified Ideographs
        (0x3400 <= cp <= 0x4DBF) or    # CJK Extension A
        (0x20000 <= cp <= 0x2A6DF) or  # CJK Extension B
        (0xF900 <= cp <= 0xFAFF) or    # CJK Compatibility Ideographs
        (0x3000 <= cp <= 0x303F) or    # CJK Symbols and Punctuation
        (0x3040 <= cp <= 0x309F) or    # Hiragana
        (0x30A0 <= cp <= 0x30FF) or    # Katakana
        (0xAC00 <= cp <= 0xD7AF) or    # Hangul Syllables
        (0x1100 <= cp <= 0x11FF) or    # Hangul Jamo
        (0xFF00 <= cp <= 0xFFEF) or    # Halfwidth and Fullwidth Forms
        (0xFE30 <= cp <= 0xFE4F)       # CJK Compatibility Forms
    )


def _contains_cjk(text: str) -> bool:
    """Check if text contains any CJK characters."""
    return any(_is_cjk_char(ch) for ch in text)


def _text_pixel_width(text: str, font) -> int:
    """Get pixel width of text with given font."""
    if not text:
        return 0
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def _wrap_text(text: str, font, max_width: int) -> list:
    """
    Wrap text with CJK support using pixel-width measurement.
    For Latin-only text, uses textwrap with estimated character width.
    For CJK or mixed text, wraps character-by-character based on pixel width.
    """
    if not text or not text.strip():
        return []

    # For pure Latin text, use standard textwrap (preserves word boundaries)
    if not _contains_cjk(text):
        avg_char_w = max(1, _text_pixel_width("M", font))
        chars_per_line = max(10, max_width // avg_char_w)
        return textwrap.wrap(text, width=chars_per_line)

    # CJK or mixed text: pixel-based character wrapping
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        if _text_pixel_width(test, font) > max_width and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return lines


# ---- Font Loading ----

def _get_font(
    font_name: str,
    size: int,
    language: Language = Language.ENGLISH,
) -> ImageFont.FreeTypeFont:
    """Load a font with multi-level fallback and CJK support."""
    # For CJK languages, prefer CJK-capable fonts first
    if language in _CJK_LANGUAGES:
        is_bold = "Bold" in font_name or "bold" in font_name
        cjk_paths = _CJK_BOLD_FONT_PATHS if is_bold else _CJK_FONT_PATHS
        for cjk_path in cjk_paths:
            if os.path.exists(cjk_path):
                try:
                    return ImageFont.truetype(cjk_path, size)
                except (OSError, IOError):
                    continue

    # Project-local fonts
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(base_dir, "data", "fonts", font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except (OSError, IOError) as e:
            logger.debug("Could not load project font %s: %s", font_path, e)

    # System font paths
    system_paths = [
        f"/usr/share/fonts/truetype/dejavu/{font_name}",
        f"/usr/share/fonts/truetype/{font_name}",
        f"/usr/share/fonts/{font_name}",
        f"/System/Library/Fonts/{font_name}",
    ]
    for path in system_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue

    # Generic name lookup
    for name in [font_name, "DejaVuSans.ttf", "Arial.ttf", "Helvetica.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue

    logger.warning("No TrueType font found, using PIL default bitmap font")
    return ImageFont.load_default()


# ---- Drawing Helpers ----

def _rgb_color(color_tuple: tuple) -> RGBColor:
    """Convert (r, g, b) tuple to pptx RGBColor."""
    return RGBColor(color_tuple[0], color_tuple[1], color_tuple[2])


def _draw_text(draw, pos, text, font, fill, shadow=False):
    """Draw text with optional drop shadow for readability over images."""
    if shadow:
        draw.text(
            (pos[0] + _SHADOW_OFFSET, pos[1] + _SHADOW_OFFSET),
            text, font=font, fill=_SHADOW_COLOR,
        )
    draw.text(pos, text, font=font, fill=fill)


def _prepare_background(
    slide_index: int,
    colors: ThemeColors,
    background_images: Optional[dict] = None,
) -> Image.Image:
    """
    Create the slide background image.
    If an AI-generated background exists for this slide, composite it with a
    semi-transparent theme overlay for text readability.
    Otherwise, return a solid-color background.
    """
    if background_images and slide_index in background_images:
        bg_path = background_images[slide_index]
        try:
            bg_img = Image.open(bg_path).resize(
                (SLIDE_WIDTH, SLIDE_HEIGHT), Image.LANCZOS
            ).convert("RGBA")
            # Semi-transparent overlay matching theme for readability
            overlay = Image.new(
                "RGBA",
                (SLIDE_WIDTH, SLIDE_HEIGHT),
                (*colors.background, BG_OVERLAY_OPACITY),
            )
            img = Image.alpha_composite(bg_img, overlay).convert("RGB")
            logger.debug("Applied AI background for slide %d", slide_index)
            return img
        except Exception as e:
            logger.warning("Could not load background for slide %d: %s", slide_index, e)

    return Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), color=colors.background)


def _add_pptx_background(slide, bg_path: str, prs: Presentation):
    """Add a background image to a PPTX slide, sent behind all content."""
    try:
        pic = slide.shapes.add_picture(
            bg_path, 0, 0, prs.slide_width, prs.slide_height
        )
        # Move picture to back (behind all other shapes)
        sp = pic._element
        sp.getparent().remove(sp)
        slide.shapes._spTree.insert(2, sp)
    except Exception as e:
        logger.warning("Could not add PPTX background: %s", e)


# ---- PPTX Slide Builders ----

def create_pptx_file(
    slides_data: List[SlideData],
    output_path: str,
    theme: SlideTheme = SlideTheme.PROFESSIONAL,
    background_images: Optional[dict] = None,
) -> str:
    """Create a themed PowerPoint file from slide data with optional AI backgrounds."""
    prs = Presentation()
    colors = THEMES.get(theme, THEMES[SlideTheme.PROFESSIONAL])

    # Set slide dimensions to 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    for i, slide_data in enumerate(slides_data):
        layout = slide_data.layout

        if layout == SlideLayout.TITLE:
            _add_title_slide(prs, slide_data, colors)
        elif layout == SlideLayout.SECTION:
            _add_section_slide(prs, slide_data, colors)
        elif layout == SlideLayout.TWO_COLUMN:
            _add_two_column_slide(prs, slide_data, colors)
        else:
            _add_content_slide(prs, slide_data, colors)

        # Add AI background image if available
        if background_images and i in background_images:
            slide = prs.slides[len(prs.slides) - 1]
            _add_pptx_background(slide, background_images[i], prs)

    prs.save(output_path)
    logger.info("PPTX saved: %s (%d slides, theme: %s)", output_path, len(slides_data), theme.value)
    return output_path


def _add_content_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a standard content slide with themed colors."""
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

    if slide.shapes.title:
        slide.shapes.title.text = slide_data.title
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.color.rgb = _rgb_color(colors.header)
                run.font.bold = True
                run.font.size = Pt(32)

    if len(slide.placeholders) > 1:
        ph = slide.placeholders[1]
        if ph.has_text_frame:
            tf = ph.text_frame
            if slide_data.content:
                tf.text = slide_data.content[0]
                for run in tf.paragraphs[0].runs:
                    run.font.size = Pt(18)
                    run.font.color.rgb = _rgb_color(colors.text)
                for point in slide_data.content[1:]:
                    p = tf.add_paragraph()
                    p.text = point
                    p.space_before = Pt(6)
                    for run in p.runs:
                        run.font.size = Pt(18)
                        run.font.color.rgb = _rgb_color(colors.text)

    if slide.has_notes_slide:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


def _add_title_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a title/cover slide."""
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)

    if slide.shapes.title:
        slide.shapes.title.text = slide_data.title
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.color.rgb = _rgb_color(colors.header)
                run.font.bold = True
                run.font.size = Pt(44)

    if len(slide.placeholders) > 1 and slide_data.content:
        subtitle_ph = slide.placeholders[1]
        if subtitle_ph.has_text_frame:
            subtitle_ph.text_frame.text = slide_data.content[0]
            for paragraph in subtitle_ph.text_frame.paragraphs:
                paragraph.alignment = PP_ALIGN.CENTER
                for run in paragraph.runs:
                    run.font.size = Pt(22)
                    run.font.color.rgb = _rgb_color(colors.accent)

    if slide.has_notes_slide:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


def _add_section_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a section divider slide."""
    slide_layout = prs.slide_layouts[2] if len(prs.slide_layouts) > 2 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)

    if slide.shapes.title:
        slide.shapes.title.text = slide_data.title
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.color.rgb = _rgb_color(colors.accent)
                run.font.bold = True
                run.font.size = Pt(40)

    if slide.has_notes_slide:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


def _add_two_column_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a two-column layout slide."""
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

    if slide.shapes.title:
        slide.shapes.title.text = slide_data.title
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.color.rgb = _rgb_color(colors.header)
                run.font.bold = True
                run.font.size = Pt(32)

    if len(slide.placeholders) > 1:
        ph = slide.placeholders[1]
        if ph.has_text_frame:
            tf = ph.text_frame
            all_content = slide_data.content
            if all_content:
                tf.text = all_content[0]
                for run in tf.paragraphs[0].runs:
                    run.font.size = Pt(18)
                    run.font.color.rgb = _rgb_color(colors.text)
                for point in all_content[1:]:
                    p = tf.add_paragraph()
                    p.text = point
                    for run in p.runs:
                        run.font.size = Pt(18)
                        run.font.color.rgb = _rgb_color(colors.text)

    if slide.has_notes_slide:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


# ---- Pillow Slide Image Renderers ----

def _draw_decorative_elements(draw: ImageDraw.Draw, theme: ThemeColors, slide_index: int, total_slides: int):
    """Draw subtle decorative elements based on theme."""
    draw.rectangle(
        [(0, HEADER_HEIGHT), (SLIDE_WIDTH, HEADER_HEIGHT + 4)],
        fill=theme.accent,
    )
    if total_slides > 1:
        progress = (slide_index + 1) / total_slides
        bar_y = SLIDE_HEIGHT - 6
        draw.rectangle([(0, bar_y), (SLIDE_WIDTH, SLIDE_HEIGHT)], fill=theme.footer)
        draw.rectangle([(0, bar_y), (int(SLIDE_WIDTH * progress), SLIDE_HEIGHT)], fill=theme.accent)


def _render_title_layout(
    draw: ImageDraw.Draw,
    slide_data: SlideData,
    colors: ThemeColors,
    title_font: ImageFont.FreeTypeFont,
    content_font: ImageFont.FreeTypeFont,
    footer_font: ImageFont.FreeTypeFont,
    slide_index: int,
    total_slides: int,
    has_bg_image: bool = False,
    language: Language = Language.ENGLISH,
):
    """Render a title/cover slide with centered content."""
    shadow = has_bg_image

    if not has_bg_image:
        draw.rectangle([(0, 0), (SLIDE_WIDTH, SLIDE_HEIGHT)], fill=colors.header)

    # Accent line
    accent_y = SLIDE_HEIGHT // 2 + 40
    draw.rectangle([(SLIDE_WIDTH // 4, accent_y), (3 * SLIDE_WIDTH // 4, accent_y + 4)], fill=colors.accent)

    # Centered title
    title = slide_data.title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    title_x = (SLIDE_WIDTH - title_w) // 2
    title_y = SLIDE_HEIGHT // 2 - title_h - 30
    title_color = (255, 255, 255) if has_bg_image else colors.title
    _draw_text(draw, (title_x, title_y), title, title_font, title_color, shadow=shadow)

    # Subtitle (first content item)
    if slide_data.content:
        subtitle = slide_data.content[0]
        bbox = draw.textbbox((0, 0), subtitle, font=content_font)
        sub_w = bbox[2] - bbox[0]
        sub_x = (SLIDE_WIDTH - sub_w) // 2
        _draw_text(draw, (sub_x, accent_y + 30), subtitle, content_font, colors.accent, shadow=shadow)

    # Footer
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    footer_color = (200, 200, 200) if has_bg_image else (*colors.title[:2], colors.title[2] // 2)
    _draw_text(
        draw, (SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45),
        footer_text, footer_font, footer_color, shadow=shadow,
    )


def _render_section_layout(
    draw: ImageDraw.Draw,
    slide_data: SlideData,
    colors: ThemeColors,
    title_font: ImageFont.FreeTypeFont,
    content_font: ImageFont.FreeTypeFont,
    footer_font: ImageFont.FreeTypeFont,
    slide_index: int,
    total_slides: int,
    has_bg_image: bool = False,
    language: Language = Language.ENGLISH,
):
    """Render a section divider slide."""
    shadow = has_bg_image

    # Left accent bar
    draw.rectangle([(0, 0), (20, SLIDE_HEIGHT)], fill=colors.accent)

    # Centered large title (uses language-aware font!)
    title = slide_data.title
    large_font = _get_font("DejaVuSans-Bold.ttf", 90, language)
    bbox = draw.textbbox((0, 0), title, font=large_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    title_x = (SLIDE_WIDTH - title_w) // 2
    title_y = (SLIDE_HEIGHT - title_h) // 2 - 20
    title_color = (255, 255, 255) if has_bg_image else colors.header
    _draw_text(draw, (title_x, title_y), title, large_font, title_color, shadow=shadow)

    # Subtle underline
    line_y = title_y + title_h + 20
    line_w = min(title_w, 600)
    line_x = (SLIDE_WIDTH - line_w) // 2
    draw.rectangle([(line_x, line_y), (line_x + line_w, line_y + 4)], fill=colors.accent)

    # Footer
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    footer_color = (200, 200, 200) if has_bg_image else colors.footer
    _draw_text(
        draw, (SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45),
        footer_text, footer_font, footer_color, shadow=shadow,
    )


def _render_two_column_layout(
    draw: ImageDraw.Draw,
    slide_data: SlideData,
    colors: ThemeColors,
    title_font: ImageFont.FreeTypeFont,
    content_font: ImageFont.FreeTypeFont,
    footer_font: ImageFont.FreeTypeFont,
    slide_index: int,
    total_slides: int,
    has_bg_image: bool = False,
    language: Language = Language.ENGLISH,
):
    """Render a two-column content slide."""
    shadow = has_bg_image

    # Header bar
    draw.rectangle([(0, 0), (SLIDE_WIDTH, HEADER_HEIGHT)], fill=colors.header)
    _draw_decorative_elements(draw, colors, slide_index, total_slides)

    # Title
    title = slide_data.title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_h = bbox[3] - bbox[1]
    title_y = (HEADER_HEIGHT - title_h) // 2
    _draw_text(draw, (MARGIN_X, title_y), title, title_font, colors.title, shadow=False)

    # Vertical divider line
    mid_x = SLIDE_WIDTH // 2
    divider_color = (200, 200, 200) if has_bg_image else colors.footer
    draw.rectangle([(mid_x - 1, CONTENT_START_Y), (mid_x + 1, SLIDE_HEIGHT - 80)], fill=divider_color)

    # Split content into two columns
    content = slide_data.content
    mid = max(1, len(content) // 2)
    left_items = content[:mid]
    right_items = content[mid:]

    for col_idx, (items, start_x) in enumerate([(left_items, MARGIN_X), (right_items, mid_x + 40)]):
        y = CONTENT_START_Y
        max_y = SLIDE_HEIGHT - 80
        for point in items:
            if y >= max_y:
                break
            wrapped = _wrap_text(point, content_font, COLUMN_MAX_WIDTH)
            for j, line in enumerate(wrapped):
                if y >= max_y:
                    break
                prefix = "\u2022 " if j == 0 else "  "
                _draw_text(draw, (start_x, y), f"{prefix}{line}", content_font, colors.text, shadow=shadow)
                y += LINE_SPACING
            y += 10

    # Footer
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    footer_color = (200, 200, 200) if has_bg_image else colors.footer
    _draw_text(
        draw, (SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45),
        footer_text, footer_font, footer_color, shadow=shadow,
    )


def _render_content_layout(
    draw: ImageDraw.Draw,
    slide_data: SlideData,
    colors: ThemeColors,
    title_font: ImageFont.FreeTypeFont,
    content_font: ImageFont.FreeTypeFont,
    footer_font: ImageFont.FreeTypeFont,
    slide_index: int,
    total_slides: int,
    has_bg_image: bool = False,
    language: Language = Language.ENGLISH,
):
    """Render a standard content slide."""
    shadow = has_bg_image

    # Header bar
    draw.rectangle([(0, 0), (SLIDE_WIDTH, HEADER_HEIGHT)], fill=colors.header)
    _draw_decorative_elements(draw, colors, slide_index, total_slides)

    # Title
    title = slide_data.title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_h = bbox[3] - bbox[1]
    title_y = (HEADER_HEIGHT - title_h) // 2
    _draw_text(draw, (MARGIN_X, title_y), title, title_font, colors.title, shadow=False)

    # Content with CJK-aware wrapping
    y = CONTENT_START_Y
    max_y = SLIDE_HEIGHT - 80
    for point in slide_data.content:
        if y >= max_y:
            _draw_text(draw, (MARGIN_X, y), "...", content_font, colors.footer, shadow=shadow)
            break
        wrapped = _wrap_text(point, content_font, CONTENT_MAX_WIDTH)
        for j, line in enumerate(wrapped):
            if y >= max_y:
                break
            prefix = "\u2022 " if j == 0 else "  "
            x = MARGIN_X if j == 0 else MARGIN_X + BULLET_INDENT
            _draw_text(draw, (x, y), f"{prefix}{line}", content_font, colors.text, shadow=shadow)
            y += LINE_SPACING
        y += 10

    # Footer
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    footer_color = (200, 200, 200) if has_bg_image else colors.footer
    _draw_text(
        draw, (SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45),
        footer_text, footer_font, footer_color, shadow=shadow,
    )


# Layout renderer dispatch
_LAYOUT_RENDERERS = {
    SlideLayout.TITLE: _render_title_layout,
    SlideLayout.SECTION: _render_section_layout,
    SlideLayout.TWO_COLUMN: _render_two_column_layout,
    SlideLayout.CONTENT: _render_content_layout,
}


def create_slide_images(
    slides_data: List[SlideData],
    output_dir: str,
    theme: SlideTheme = SlideTheme.PROFESSIONAL,
    background_images: Optional[dict] = None,
    language: Language = Language.ENGLISH,
) -> List[str]:
    """
    Render high-quality slide images using Pillow.
    Supports themes, layouts, AI background images, CJK fonts, and text shadows.
    """
    os.makedirs(output_dir, exist_ok=True)
    colors = THEMES.get(theme, THEMES[SlideTheme.PROFESSIONAL])
    image_paths = []

    title_font = _get_font("DejaVuSans-Bold.ttf", TITLE_FONT_SIZE, language)
    content_font = _get_font("DejaVuSans.ttf", CONTENT_FONT_SIZE, language)
    footer_font = _get_font("DejaVuSans.ttf", FOOTER_FONT_SIZE, language)

    total_slides = len(slides_data)

    for i, slide_data in enumerate(slides_data):
        img = _prepare_background(i, colors, background_images)
        draw = ImageDraw.Draw(img)

        has_bg = background_images is not None and i in background_images
        renderer = _LAYOUT_RENDERERS.get(slide_data.layout, _render_content_layout)
        renderer(
            draw, slide_data, colors, title_font, content_font, footer_font,
            i, total_slides, has_bg_image=has_bg, language=language,
        )

        filename = f"slide_{i + 1:03d}.png"
        path = os.path.join(output_dir, filename)
        img.save(path, "PNG", optimize=True)
        image_paths.append(path)

    bg_count = len(background_images) if background_images else 0
    logger.info(
        "Rendered %d slide images (theme: %s, bg_images: %d, lang: %s)",
        len(image_paths), theme.value, bg_count, language.value,
    )
    return image_paths


def create_pdf_from_images(image_paths: List[str], output_path: str) -> str:
    """Compile slide images into a single PDF document."""
    if not image_paths:
        raise ValueError("No images provided for PDF generation")

    images = [Image.open(p).convert("RGB") for p in image_paths]
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        resolution=300,
    )
    logger.info("PDF saved: %s (%d pages)", output_path, len(images))
    return output_path
