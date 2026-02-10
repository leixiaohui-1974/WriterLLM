"""
Slide rendering module - generates PPTX, slide images, and PDF output.
Supports multiple visual themes, slide layouts, and themed PPTX output.
"""
import os
import logging
import textwrap
from typing import List

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFont

from src.models import SlideData, SlideLayout, SlideTheme, ThemeColors, THEMES
from src.config import (
    SLIDE_WIDTH, SLIDE_HEIGHT,
    TITLE_FONT_SIZE, CONTENT_FONT_SIZE, FOOTER_FONT_SIZE,
    TEXT_WRAP_WIDTH,
)

logger = logging.getLogger(__name__)

# Layout constants
MARGIN_X = 100
HEADER_HEIGHT = 200
CONTENT_START_Y = 280
LINE_SPACING = 75
BULLET_INDENT = 30


def _get_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a font with multi-level fallback."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(base_dir, "data", "fonts", font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except (OSError, IOError) as e:
            logger.debug("Could not load project font %s: %s", font_path, e)

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

    for name in [font_name, "DejaVuSans.ttf", "Arial.ttf", "Helvetica.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue

    logger.warning("No TrueType font found, using PIL default bitmap font")
    return ImageFont.load_default()


def _rgb_color(color_tuple: tuple) -> RGBColor:
    """Convert (r, g, b) tuple to pptx RGBColor."""
    return RGBColor(color_tuple[0], color_tuple[1], color_tuple[2])


def create_pptx_file(
    slides_data: List[SlideData],
    output_path: str,
    theme: SlideTheme = SlideTheme.PROFESSIONAL,
) -> str:
    """Create a themed PowerPoint file from slide data."""
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

    prs.save(output_path)
    logger.info("PPTX saved: %s (%d slides, theme: %s)", output_path, len(slides_data), theme.value)
    return output_path


def _add_content_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a standard content slide with themed colors."""
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)

    # Style the title
    if slide.shapes.title:
        slide.shapes.title.text = slide_data.title
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.color.rgb = _rgb_color(colors.header)
                run.font.bold = True
                run.font.size = Pt(32)

    # Style the content
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

    # Speaker Notes
    if slide.has_notes_slide:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


def _add_title_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a title/cover slide."""
    slide_layout = prs.slide_layouts[0]  # Title Slide
    slide = prs.slides.add_slide(slide_layout)

    if slide.shapes.title:
        slide.shapes.title.text = slide_data.title
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.color.rgb = _rgb_color(colors.header)
                run.font.bold = True
                run.font.size = Pt(44)

    # Subtitle from first content item
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

    # Split content into two columns
    if len(slide.placeholders) > 1:
        ph = slide.placeholders[1]
        if ph.has_text_frame:
            tf = ph.text_frame
            mid = len(slide_data.content) // 2
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


def _draw_decorative_elements(draw: ImageDraw.Draw, theme: ThemeColors, slide_index: int, total_slides: int):
    """Draw subtle decorative elements based on theme."""
    # Accent line under header
    draw.rectangle(
        [(0, HEADER_HEIGHT), (SLIDE_WIDTH, HEADER_HEIGHT + 4)],
        fill=theme.accent,
    )

    # Progress indicator at bottom
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
):
    """Render a title/cover slide with centered content."""
    # Full-slide header background
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
    draw.text((title_x, title_y), title, font=title_font, fill=colors.title)

    # Subtitle (first content item)
    if slide_data.content:
        subtitle = slide_data.content[0]
        bbox = draw.textbbox((0, 0), subtitle, font=content_font)
        sub_w = bbox[2] - bbox[0]
        sub_x = (SLIDE_WIDTH - sub_w) // 2
        draw.text((sub_x, accent_y + 30), subtitle, font=content_font, fill=colors.accent)

    # Footer
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    draw.text(
        (SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45),
        footer_text, font=footer_font, fill=(*colors.title[:2], colors.title[2] // 2),
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
):
    """Render a section divider slide."""
    # Left accent bar
    draw.rectangle([(0, 0), (20, SLIDE_HEIGHT)], fill=colors.accent)

    # Centered large title
    title = slide_data.title
    large_font = _get_font("DejaVuSans-Bold.ttf", 90)
    bbox = draw.textbbox((0, 0), title, font=large_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    title_x = (SLIDE_WIDTH - title_w) // 2
    title_y = (SLIDE_HEIGHT - title_h) // 2 - 20
    draw.text((title_x, title_y), title, font=large_font, fill=colors.header)

    # Subtle underline
    line_y = title_y + title_h + 20
    line_w = min(title_w, 600)
    line_x = (SLIDE_WIDTH - line_w) // 2
    draw.rectangle([(line_x, line_y), (line_x + line_w, line_y + 4)], fill=colors.accent)

    # Footer
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    draw.text((SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45), footer_text, font=footer_font, fill=colors.footer)


def _render_two_column_layout(
    draw: ImageDraw.Draw,
    slide_data: SlideData,
    colors: ThemeColors,
    title_font: ImageFont.FreeTypeFont,
    content_font: ImageFont.FreeTypeFont,
    footer_font: ImageFont.FreeTypeFont,
    slide_index: int,
    total_slides: int,
):
    """Render a two-column content slide."""
    # Header bar
    draw.rectangle([(0, 0), (SLIDE_WIDTH, HEADER_HEIGHT)], fill=colors.header)
    _draw_decorative_elements(draw, colors, slide_index, total_slides)

    # Title
    title = slide_data.title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_h = bbox[3] - bbox[1]
    title_y = (HEADER_HEIGHT - title_h) // 2
    draw.text((MARGIN_X, title_y), title, font=title_font, fill=colors.title)

    # Vertical divider line
    mid_x = SLIDE_WIDTH // 2
    draw.rectangle([(mid_x - 1, CONTENT_START_Y), (mid_x + 1, SLIDE_HEIGHT - 80)], fill=colors.footer)

    # Split content into two columns
    content = slide_data.content
    mid = max(1, len(content) // 2)
    left_items = content[:mid]
    right_items = content[mid:]
    col_wrap = TEXT_WRAP_WIDTH // 2 + 5

    for col_idx, (items, start_x) in enumerate([(left_items, MARGIN_X), (right_items, mid_x + 40)]):
        y = CONTENT_START_Y
        max_y = SLIDE_HEIGHT - 80
        for point in items:
            if y >= max_y:
                break
            wrapped = textwrap.wrap(point, width=col_wrap)
            for j, line in enumerate(wrapped):
                if y >= max_y:
                    break
                prefix = "\u2022 " if j == 0 else "  "
                draw.text((start_x, y), f"{prefix}{line}", font=content_font, fill=colors.text)
                y += LINE_SPACING
            y += 10

    # Footer
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    draw.text((SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45), footer_text, font=footer_font, fill=colors.footer)


def _render_content_layout(
    draw: ImageDraw.Draw,
    slide_data: SlideData,
    colors: ThemeColors,
    title_font: ImageFont.FreeTypeFont,
    content_font: ImageFont.FreeTypeFont,
    footer_font: ImageFont.FreeTypeFont,
    slide_index: int,
    total_slides: int,
):
    """Render a standard content slide."""
    # Header bar
    draw.rectangle([(0, 0), (SLIDE_WIDTH, HEADER_HEIGHT)], fill=colors.header)
    _draw_decorative_elements(draw, colors, slide_index, total_slides)

    # Title
    title = slide_data.title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_h = bbox[3] - bbox[1]
    title_y = (HEADER_HEIGHT - title_h) // 2
    draw.text((MARGIN_X, title_y), title, font=title_font, fill=colors.title)

    # Content
    y = CONTENT_START_Y
    max_y = SLIDE_HEIGHT - 80
    for point in slide_data.content:
        if y >= max_y:
            draw.text((MARGIN_X, y), "...", font=content_font, fill=colors.footer)
            break
        wrapped = textwrap.wrap(point, width=TEXT_WRAP_WIDTH)
        for j, line in enumerate(wrapped):
            if y >= max_y:
                break
            prefix = "\u2022 " if j == 0 else "  "
            x = MARGIN_X if j == 0 else MARGIN_X + BULLET_INDENT
            draw.text((x, y), f"{prefix}{line}", font=content_font, fill=colors.text)
            y += LINE_SPACING
        y += 10

    # Footer
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    draw.text((SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45), footer_text, font=footer_font, fill=colors.footer)


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
) -> List[str]:
    """
    Render high-quality slide images using Pillow.
    Supports multiple themes and layout types.
    """
    os.makedirs(output_dir, exist_ok=True)
    colors = THEMES.get(theme, THEMES[SlideTheme.PROFESSIONAL])
    image_paths = []

    title_font = _get_font("DejaVuSans-Bold.ttf", TITLE_FONT_SIZE)
    content_font = _get_font("DejaVuSans.ttf", CONTENT_FONT_SIZE)
    footer_font = _get_font("DejaVuSans.ttf", FOOTER_FONT_SIZE)

    total_slides = len(slides_data)

    for i, slide_data in enumerate(slides_data):
        img = Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), color=colors.background)
        draw = ImageDraw.Draw(img)

        renderer = _LAYOUT_RENDERERS.get(slide_data.layout, _render_content_layout)
        renderer(draw, slide_data, colors, title_font, content_font, footer_font, i, total_slides)

        filename = f"slide_{i + 1:03d}.png"
        path = os.path.join(output_dir, filename)
        img.save(path, "PNG", optimize=True)
        image_paths.append(path)

    logger.info("Rendered %d slide images (theme: %s)", len(image_paths), theme.value)
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
        resolution=150,
    )
    logger.info("PDF saved: %s (%d pages)", output_path, len(images))
    return output_path
