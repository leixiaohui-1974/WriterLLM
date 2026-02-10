"""
Slide rendering module - generates PPTX, slide images, and PDF output.
Supports multiple visual themes and improved layout engine.
"""
import os
import logging
import textwrap
from typing import List

from pptx import Presentation
from pptx.util import Pt
from PIL import Image, ImageDraw, ImageFont

from src.models import SlideData, SlideTheme, ThemeColors, THEMES
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
    # 1. Try project-local fonts
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(base_dir, "data", "fonts", font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except (OSError, IOError) as e:
            logger.debug("Could not load project font %s: %s", font_path, e)

    # 2. Try common system font paths
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

    # 3. Try by name (PIL's built-in search)
    for name in [font_name, "DejaVuSans.ttf", "Arial.ttf", "Helvetica.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue

    # 4. Last resort: PIL default
    logger.warning("No TrueType font found, using PIL default bitmap font")
    return ImageFont.load_default()


def create_pptx_file(slides_data: List[SlideData], output_path: str) -> str:
    """Create a PowerPoint file from slide data."""
    prs = Presentation()

    for slide_data in slides_data:
        slide_layout = prs.slide_layouts[1]  # 'Title and Content' layout
        slide = prs.slides.add_slide(slide_layout)

        if slide.shapes.title:
            slide.shapes.title.text = slide_data.title

        if len(slide.placeholders) > 1:
            ph = slide.placeholders[1]
            if ph.has_text_frame:
                tf = ph.text_frame
                if slide_data.content:
                    tf.text = slide_data.content[0]
                    for point in slide_data.content[1:]:
                        p = tf.add_paragraph()
                        p.text = point

        if slide.has_notes_slide:
            notes_tf = slide.notes_slide.notes_text_frame
            notes_tf.text = slide_data.speaker_notes

    prs.save(output_path)
    logger.info("PPTX saved: %s", output_path)
    return output_path


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


def create_slide_images(
    slides_data: List[SlideData],
    output_dir: str,
    theme: SlideTheme = SlideTheme.PROFESSIONAL,
) -> List[str]:
    """
    Render high-quality slide images using Pillow.
    Supports multiple themes with improved layout.
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

        # Header bar
        draw.rectangle([(0, 0), (SLIDE_WIDTH, HEADER_HEIGHT)], fill=colors.header)

        # Decorative elements
        _draw_decorative_elements(draw, colors, i, total_slides)

        # Title (vertically centered in header)
        title = slide_data.title
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_h = bbox[3] - bbox[1]
        title_y = (HEADER_HEIGHT - title_h) // 2
        draw.text((MARGIN_X, title_y), title, font=title_font, fill=colors.title)

        # Content with improved wrapping
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

            y += 10  # Extra spacing between bullet groups

        # Footer
        footer_text = f"Slide {i + 1} / {total_slides}"
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        footer_w = bbox[2] - bbox[0]
        draw.text(
            (SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45),
            footer_text,
            font=footer_font,
            fill=colors.footer,
        )

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
