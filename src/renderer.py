"""
Slide rendering module - generates PPTX, slide images, and PDF output.
Supports multiple visual themes, slide layouts, themed PPTX output,
AI background image compositing, CJK text wrapping, text shadows,
and responsive font sizing.
"""
import os
import logging
import textwrap
from typing import List, Optional

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
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
FOOTER_AREA = 80  # reserved space at bottom for footer

# Available pixel widths for text content
CONTENT_MAX_WIDTH = SLIDE_WIDTH - 2 * MARGIN_X       # ~1720px for full-width content
COLUMN_MAX_WIDTH = SLIDE_WIDTH // 2 - MARGIN_X - 40  # ~820px per column

# Text shadow settings
_SHADOW_OFFSET = 2
_SHADOW_COLOR = (0, 0, 0)

# Responsive font sizing bounds
_MIN_CONTENT_FONT_SIZE = 24
_FONT_SIZE_STEP = 3

# Bullet styling: themed icons cycle per bullet index
_BULLET_ICONS = ["\u25B8", "\u25B8", "\u25B8", "\u25B8"]  # Right-pointing triangles

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


# ---- Responsive Font Sizing ----

def _estimate_content_lines(content: list, font, max_width: int) -> int:
    """Estimate total rendered lines for a list of bullet points."""
    total = 0
    for point in content:
        wrapped = _wrap_text(point, font, max_width)
        total += max(len(wrapped), 1)
    return total


def _compute_content_font_size(
    content: list,
    language: Language,
    max_width: int,
    available_height: int,
    base_size: int = CONTENT_FONT_SIZE,
) -> int:
    """
    Compute the largest font size that fits all content within available_height.
    Shrinks from base_size down to _MIN_CONTENT_FONT_SIZE in steps.
    """
    size = base_size
    while size >= _MIN_CONTENT_FONT_SIZE:
        font = _get_font("DejaVuSans.ttf", size, language)
        line_h = int(size * 1.67)  # LINE_SPACING scales with font size
        total_lines = _estimate_content_lines(content, font, max_width)
        # Add ~10px gap per bullet
        needed = total_lines * line_h + len(content) * 10
        if needed <= available_height:
            return size
        size -= _FONT_SIZE_STEP
    return _MIN_CONTENT_FONT_SIZE


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


def _draw_gradient_rect(img: Image.Image, rect: tuple, color_top: tuple, color_bottom: tuple):
    """Draw a vertical gradient rectangle onto an image (in-place)."""
    x0, y0, x1, y1 = rect
    h = max(1, y1 - y0)
    for row in range(h):
        t = row / h
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * t)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * t)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * t)
        draw = ImageDraw.Draw(img)
        draw.line([(x0, y0 + row), (x1, y0 + row)], fill=(r, g, b))


def _fit_title_in_header(
    title: str, title_font, language: Language, max_width: int, base_size: int = TITLE_FONT_SIZE,
) -> tuple:
    """
    Wrap and optionally shrink a title to fit within max_width.
    Returns (lines, font) where lines is a list of wrapped title lines.
    """
    min_size = 40
    size = base_size
    font = title_font
    while size >= min_size:
        lines = _wrap_text(title, font, max_width)
        if len(lines) <= 2:
            return lines, font
        size -= 4
        font = _get_font("DejaVuSans-Bold.ttf", size, language)
    # At minimum size, just wrap and accept
    return _wrap_text(title, font, max_width)[:2], font


def _prepare_background(
    slide_index: int,
    colors: ThemeColors,
    background_images: Optional[dict] = None,
    overlay_opacity: int = BG_OVERLAY_OPACITY,
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
            bg_img = Image.open(bg_path).convert("RGBA")
            # Preserve aspect ratio by cover-cropping
            bg_img = _cover_crop(bg_img, SLIDE_WIDTH, SLIDE_HEIGHT)
            # Semi-transparent overlay matching theme for readability
            overlay = Image.new(
                "RGBA",
                (SLIDE_WIDTH, SLIDE_HEIGHT),
                (*colors.background, overlay_opacity),
            )
            img = Image.alpha_composite(bg_img, overlay).convert("RGB")
            logger.debug("Applied AI background for slide %d", slide_index)
            return img
        except Exception as e:
            logger.warning("Could not load background for slide %d: %s", slide_index, e)

    return Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), color=colors.background)


def _cover_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize image to cover target size while preserving aspect ratio, then center-crop."""
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    # Center crop
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


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

def _set_pptx_slide_background(slide, color: tuple):
    """Set a solid background fill color on a PPTX slide."""
    try:
        from pptx.oxml.ns import qn
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = _rgb_color(color)
    except Exception as e:
        logger.debug("Could not set slide background: %s", e)


# Supported PPTX transition types (OpenXML element names)
PPTX_TRANSITION_TYPES = ["fade", "push", "wipe", "cover", "split", "dissolve"]


def _add_pptx_slide_transition(slide, duration_ms: int = 700, transition_type: str = "fade"):
    """Add a slide transition with configurable duration and type."""
    try:
        from lxml import etree
        transition = etree.SubElement(
            slide._element,
            qn("p:transition"),
            attrib={"advClick": "1", "dur": str(duration_ms)},
        )
        # Map type name to OpenXML element
        type_map = {
            "fade": "p:fade",
            "push": "p:push",
            "wipe": "p:wipe",
            "cover": "p:cover",
            "split": "p:split",
            "dissolve": "p:dissolve",
        }
        element_name = type_map.get(transition_type, "p:fade")
        etree.SubElement(transition, qn(element_name))
    except Exception as e:
        logger.debug("Could not add slide transition: %s", e)


def _add_pptx_slide_number(slide, slide_index: int, total_slides: int, colors: ThemeColors,
                           footer_company: str = "", footer_author: str = ""):
    """Add a slide number and optional branding footer to a PPTX slide."""
    try:
        from pptx.util import Inches, Pt, Emu

        # Footer text box: right-aligned slide number
        footer_text = f"Slide {slide_index + 1} / {total_slides}"

        # Slide number at bottom-right
        txBox = slide.shapes.add_textbox(
            Inches(10.5), Inches(6.9), Inches(2.5), Inches(0.4),
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        run = p.add_run()
        run.text = footer_text
        run.font.size = Pt(10)
        run.font.color.rgb = _rgb_color(colors.footer)

        # Company branding at bottom-left (truncate long names)
        if footer_company:
            company_text = (footer_company[:45] + "\u2026") if len(footer_company) > 48 else footer_company
            txBox2 = slide.shapes.add_textbox(
                Inches(0.4), Inches(6.9), Inches(4.0), Inches(0.4),
            )
            tf2 = txBox2.text_frame
            tf2.word_wrap = False
            p2 = tf2.paragraphs[0]
            p2.alignment = PP_ALIGN.LEFT
            run2 = p2.add_run()
            run2.text = company_text
            run2.font.size = Pt(10)
            run2.font.color.rgb = _rgb_color(colors.footer)

        # Author at bottom-center (truncate long names)
        if footer_author:
            author_text = (footer_author[:45] + "\u2026") if len(footer_author) > 48 else footer_author
            txBox3 = slide.shapes.add_textbox(
                Inches(4.5), Inches(6.9), Inches(4.0), Inches(0.4),
            )
            tf3 = txBox3.text_frame
            tf3.word_wrap = False
            p3 = tf3.paragraphs[0]
            p3.alignment = PP_ALIGN.CENTER
            run3 = p3.add_run()
            run3.text = author_text
            run3.font.size = Pt(10)
            run3.font.color.rgb = _rgb_color(colors.footer)
    except Exception as e:
        logger.debug("Could not add slide number: %s", e)


def create_pptx_file(
    slides_data: List[SlideData],
    output_path: str,
    theme: SlideTheme = SlideTheme.PROFESSIONAL,
    background_images: Optional[dict] = None,
    footer_company: str = "",
    footer_author: str = "",
    enable_animations: bool = True,
    transition_duration_ms: int = 700,
    transition_type: str = "fade",
) -> str:
    """Create a themed PowerPoint file from slide data with optional AI backgrounds."""
    prs = Presentation()
    colors = THEMES.get(theme, THEMES[SlideTheme.PROFESSIONAL])

    # Set slide dimensions to 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    total_slides = len(slides_data)
    for i, slide_data in enumerate(slides_data):
        layout = slide_data.layout

        if layout == SlideLayout.TITLE:
            _add_title_slide(prs, slide_data, colors)
        elif layout == SlideLayout.SECTION:
            _add_section_slide(prs, slide_data, colors, slide_index=i)
        elif layout == SlideLayout.TWO_COLUMN:
            _add_two_column_slide(prs, slide_data, colors)
            _set_pptx_slide_background(prs.slides[len(prs.slides) - 1], colors.background)
        else:
            _add_content_slide(prs, slide_data, colors)
            _set_pptx_slide_background(prs.slides[len(prs.slides) - 1], colors.background)

        # Add AI background image if available (overrides solid background)
        has_bg_image = background_images and i in background_images
        if has_bg_image:
            slide = prs.slides[len(prs.slides) - 1]
            _add_pptx_background(slide, background_images[i], prs)
            # Add text shadows for readability on background images
            for shape in prs.slides[len(prs.slides) - 1].shapes:
                if shape.has_text_frame and shape.text_frame.text.strip():
                    _add_pptx_text_shadow(shape)

        # Add slide transition and footer
        current_slide = prs.slides[len(prs.slides) - 1]
        _add_pptx_slide_transition(current_slide, duration_ms=transition_duration_ms, transition_type=transition_type)
        _add_pptx_slide_number(
            current_slide, i, total_slides, colors,
            footer_company=footer_company, footer_author=footer_author,
        )
        _add_pptx_progress_bar(current_slide, i, total_slides, colors)

        # Add bullet-by-bullet entrance animations for content slides
        if enable_animations and layout in (SlideLayout.CONTENT, SlideLayout.TWO_COLUMN):
            # For content slides, animate placeholder[1]; for two-column, animate text boxes
            animated = False
            if len(current_slide.placeholders) > 1:
                ph = current_slide.placeholders[1]
                if ph.has_text_frame:
                    num_paras = len(ph.text_frame.paragraphs)
                    if num_paras > 0:
                        _add_pptx_entrance_animations(
                            current_slide, ph.shape_id, num_paras,
                        )
                        animated = True
            # Fallback: animate text box shapes (for blank-layout two-column)
            if not animated:
                for shape in current_slide.shapes:
                    if shape.has_text_frame and shape.text_frame.text.strip():
                        num_paras = len(shape.text_frame.paragraphs)
                        if num_paras > 1:
                            _add_pptx_entrance_animations(
                                current_slide, shape.shape_id, num_paras,
                            )
                            break  # animate the first multi-paragraph text box

    prs.save(output_path)
    logger.info("PPTX saved: %s (%d slides, theme: %s)", output_path, len(slides_data), theme.value)
    return output_path


def _add_pptx_entrance_animations(slide, content_shape_id: int, num_paragraphs: int):
    """Add click-to-appear entrance animations for each bullet paragraph in a shape."""
    if num_paragraphs <= 0:
        return
    try:
        from lxml import etree

        # Build p:timing > p:tnLst > p:par (root) > p:cTn (tmRoot)
        timing = etree.SubElement(slide._element, qn("p:timing"))
        tnLst = etree.SubElement(timing, qn("p:tnLst"))
        par_root = etree.SubElement(tnLst, qn("p:par"))
        cTn_root = etree.SubElement(par_root, qn("p:cTn"), attrib={
            "id": "1", "dur": "indefinite", "restart": "never", "nodeType": "tmRoot",
        })
        childTnLst_root = etree.SubElement(cTn_root, qn("p:childTnLst"))

        # Main sequence
        seq = etree.SubElement(childTnLst_root, qn("p:seq"), attrib={
            "concurrent": "1", "nextAc": "seek",
        })
        cTn_seq = etree.SubElement(seq, qn("p:cTn"), attrib={
            "id": "2", "dur": "indefinite", "nodeType": "mainSeq",
        })
        childTnLst_seq = etree.SubElement(cTn_seq, qn("p:childTnLst"))

        anim_id = 3
        for para_idx in range(num_paragraphs):
            # Each paragraph: par > cTn > childTnLst > par > cTn > childTnLst > par > cTn (clickEffect)
            par1 = etree.SubElement(childTnLst_seq, qn("p:par"))
            cTn1 = etree.SubElement(par1, qn("p:cTn"), attrib={
                "id": str(anim_id), "fill": "hold",
            })
            anim_id += 1
            stCond1 = etree.SubElement(cTn1, qn("p:stCondLst"))
            etree.SubElement(stCond1, qn("p:cond"), attrib={"delay": "0"})

            child1 = etree.SubElement(cTn1, qn("p:childTnLst"))
            par2 = etree.SubElement(child1, qn("p:par"))
            cTn2 = etree.SubElement(par2, qn("p:cTn"), attrib={
                "id": str(anim_id), "fill": "hold",
            })
            anim_id += 1
            stCond2 = etree.SubElement(cTn2, qn("p:stCondLst"))
            etree.SubElement(stCond2, qn("p:cond"), attrib={"delay": "0"})

            child2 = etree.SubElement(cTn2, qn("p:childTnLst"))
            par3 = etree.SubElement(child2, qn("p:par"))
            cTn3 = etree.SubElement(par3, qn("p:cTn"), attrib={
                "id": str(anim_id), "presetID": "1", "presetClass": "entr",
                "presetSubtype": "0", "fill": "hold", "nodeType": "clickEffect",
            })
            anim_id += 1
            stCond3 = etree.SubElement(cTn3, qn("p:stCondLst"))
            etree.SubElement(stCond3, qn("p:cond"), attrib={"delay": "0"})

            # Set visibility to visible
            child3 = etree.SubElement(cTn3, qn("p:childTnLst"))
            set_elem = etree.SubElement(child3, qn("p:set"))
            cBhvr = etree.SubElement(set_elem, qn("p:cBhvr"))
            cTn4 = etree.SubElement(cBhvr, qn("p:cTn"), attrib={
                "id": str(anim_id), "dur": "1", "fill": "hold",
            })
            anim_id += 1
            stCond4 = etree.SubElement(cTn4, qn("p:stCondLst"))
            etree.SubElement(stCond4, qn("p:cond"), attrib={"delay": "0"})

            # Target element: specific paragraph in the shape
            tgtEl = etree.SubElement(cBhvr, qn("p:tgtEl"))
            spTgt = etree.SubElement(tgtEl, qn("p:spTgt"), attrib={
                "spid": str(content_shape_id),
            })
            txEl = etree.SubElement(spTgt, qn("p:txEl"))
            etree.SubElement(txEl, qn("p:pRg"), attrib={
                "st": str(para_idx), "end": str(para_idx),
            })

            attrNameLst = etree.SubElement(cBhvr, qn("p:attrNameLst"))
            attrName = etree.SubElement(attrNameLst, qn("p:attrName"))
            attrName.text = "style.visibility"

            to_elem = etree.SubElement(set_elem, qn("p:to"))
            etree.SubElement(to_elem, qn("p:strVal"), attrib={"val": "visible"})

        # Navigation conditions for the sequence
        prevCondLst = etree.SubElement(seq, qn("p:prevCondLst"))
        prevCond = etree.SubElement(prevCondLst, qn("p:cond"), attrib={
            "evt": "onPrev", "delay": "0",
        })
        prevTgt = etree.SubElement(prevCond, qn("p:tgtEl"))
        etree.SubElement(prevTgt, qn("p:sldTgt"))

        nextCondLst = etree.SubElement(seq, qn("p:nextCondLst"))
        nextCond = etree.SubElement(nextCondLst, qn("p:cond"), attrib={
            "evt": "onNext", "delay": "0",
        })
        nextTgt = etree.SubElement(nextCond, qn("p:tgtEl"))
        etree.SubElement(nextTgt, qn("p:sldTgt"))

    except Exception as e:
        logger.debug("Could not add entrance animations: %s", e)


def _add_pptx_header_bar(slide, colors: ThemeColors):
    """Add a header bar shape with gradient fill and accent line to a PPTX slide."""
    try:
        from lxml import etree

        # Header rectangle (~1.4 inches matches 200/1080 ratio of image renderer)
        header_bar = slide.shapes.add_shape(
            1,  # MSO_SHAPE.RECTANGLE
            Inches(0), Inches(0), Inches(13.333), Inches(1.4),
        )
        header_bar.line.fill.background()

        # Apply gradient fill via OpenXML (top color -> lighter bottom)
        r, g, b = colors.header
        r2 = min(r + 30, 255)
        g2 = min(g + 30, 255)
        b2 = min(b + 30, 255)
        sp_pr = header_bar._element.find(qn("p:spPr"))
        if sp_pr is None:
            sp_pr = header_bar._element.find(qn("a:spPr"))
        if sp_pr is None:
            sp_pr = header_bar._element.makeelement(qn("p:spPr"), {})
            header_bar._element.append(sp_pr)
        # Remove any existing fill
        for child in list(sp_pr):
            tag_local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag_local in ("solidFill", "gradFill", "noFill"):
                sp_pr.remove(child)
        grad_xml = (
            f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<a:gsLst>'
            f'<a:gs pos="0"><a:srgbClr val="{r:02X}{g:02X}{b:02X}"/></a:gs>'
            f'<a:gs pos="100000"><a:srgbClr val="{r2:02X}{g2:02X}{b2:02X}"/></a:gs>'
            f'</a:gsLst>'
            f'<a:lin ang="5400000" scaled="1"/>'
            f'</a:gradFill>'
        )
        grad_elem = etree.fromstring(grad_xml)
        sp_pr.append(grad_elem)

        # Move header to back
        sp = header_bar._element
        sp.getparent().remove(sp)
        slide.shapes._spTree.insert(2, sp)

        # Accent line below header
        accent_line = slide.shapes.add_shape(
            1,  # MSO_SHAPE.RECTANGLE
            Inches(0), Inches(1.4), Inches(13.333), Inches(0.03),
        )
        accent_line.fill.solid()
        accent_line.fill.fore_color.rgb = _rgb_color(colors.accent)
        accent_line.line.fill.background()
    except Exception:
        pass


def _add_pptx_progress_bar(slide, slide_index: int, total_slides: int, colors: ThemeColors):
    """Add a thin progress bar at the bottom of a PPTX slide."""
    if total_slides <= 1:
        return
    try:
        progress = (slide_index + 1) / total_slides
        bar_height = Inches(0.04)
        bar_y = Inches(7.5) - bar_height  # bottom of slide

        # Background bar (footer color)
        bg_bar = slide.shapes.add_shape(
            1, Inches(0), bar_y, Inches(13.333), bar_height,
        )
        bg_bar.fill.solid()
        bg_bar.fill.fore_color.rgb = _rgb_color(colors.footer)
        bg_bar.line.fill.background()

        # Progress bar (accent color)
        prog_width = Inches(13.333 * progress)
        prog_bar = slide.shapes.add_shape(
            1, Inches(0), bar_y, prog_width, bar_height,
        )
        prog_bar.fill.solid()
        prog_bar.fill.fore_color.rgb = _rgb_color(colors.accent)
        prog_bar.line.fill.background()
    except Exception:
        pass


def _compute_pptx_font_size(content: list, base_size: int = 18, min_size: int = 12) -> int:
    """Compute responsive font size for PPTX based on content density.

    Shrinks font when there are many bullets or long text to prevent overflow.
    """
    total_chars = sum(len(item) for item in content)
    num_items = len(content)

    # Thresholds for shrinking (approximate line count heuristic)
    if num_items > 8 or total_chars > 600:
        return max(min_size, base_size - 6)
    if num_items > 6 or total_chars > 400:
        return max(min_size, base_size - 4)
    if num_items > 4 or total_chars > 250:
        return max(min_size, base_size - 2)
    return base_size


def _populate_pptx_bullets(text_frame, items: list, colors: ThemeColors, font_size: int):
    """Populate a PPTX text frame with styled bullet items. Shared by content and two-column slides."""
    if not items:
        return
    text_frame.text = items[0]
    text_frame.paragraphs[0].space_before = Pt(6)
    for run in text_frame.paragraphs[0].runs:
        run.font.size = Pt(font_size)
        run.font.color.rgb = _rgb_color(colors.text)
    _format_pptx_bullet(text_frame.paragraphs[0], colors)
    for point in items[1:]:
        p = text_frame.add_paragraph()
        p.text = point
        p.space_before = Pt(6)
        for run in p.runs:
            run.font.size = Pt(font_size)
            run.font.color.rgb = _rgb_color(colors.text)
        _format_pptx_bullet(p, colors)


def _add_pptx_text_shadow(shape):
    """Add a drop shadow effect to all text in a PPTX shape for readability on background images."""
    try:
        from lxml import etree
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                rPr = run._r.get_or_add_rPr()
                # Remove existing effect list
                for child in list(rPr):
                    tag_local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                    if tag_local == "effectLst":
                        rPr.remove(child)
                shadow_xml = (
                    '<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                    '<a:outerShdw blurRad="38100" dist="19050" dir="2700000" algn="tl">'
                    '<a:srgbClr val="000000"><a:alpha val="60000"/></a:srgbClr>'
                    '</a:outerShdw>'
                    '</a:effectLst>'
                )
                rPr.append(etree.fromstring(shadow_xml))
    except Exception:
        pass


def _format_pptx_bullet(paragraph, colors: ThemeColors):
    """Apply accent-colored bullet formatting to a PPTX paragraph."""
    try:
        pPr = paragraph._pPr
        if pPr is None:
            pPr = paragraph._p.get_or_add_pPr()
        buChar = pPr.makeelement(qn("a:buChar"), {"char": "\u25B8"})
        buClr = pPr.makeelement(qn("a:buClr"), {})
        srgbClr = buClr.makeelement(
            qn("a:srgbClr"),
            {"val": f"{colors.accent[0]:02X}{colors.accent[1]:02X}{colors.accent[2]:02X}"},
        )
        buClr.append(srgbClr)
        # Remove existing bullet elements if any
        for child in list(pPr):
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag.startswith("bu"):
                pPr.remove(child)
        pPr.append(buClr)
        pPr.append(buChar)
    except Exception:
        pass  # Fallback to default bullets silently


def _add_content_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a standard content slide with themed colors, header bar, and accent bullets."""
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

    # Gradient-style header bar for visual parity with image renderer
    _add_pptx_header_bar(slide, colors)

    if slide.shapes.title:
        slide.shapes.title.text = slide_data.title
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.color.rgb = _rgb_color(colors.title)
                run.font.bold = True
                run.font.size = Pt(32)

    if len(slide.placeholders) > 1:
        ph = slide.placeholders[1]
        if ph.has_text_frame and slide_data.content:
            font_size = _compute_pptx_font_size(slide_data.content, base_size=18, min_size=12)
            _populate_pptx_bullets(ph.text_frame, slide_data.content, colors, font_size)

    if slide_data.speaker_notes:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


def _add_title_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a title/cover slide with gradient background and accent line."""
    slide_layout = prs.slide_layouts[5]  # blank layout for full control
    slide = prs.slides.add_slide(slide_layout)

    # Full-slide gradient background (header -> lighter shade)
    try:
        from lxml import etree
        bg_rect = slide.shapes.add_shape(
            1, Inches(0), Inches(0), Inches(13.333), Inches(7.5),
        )
        bg_rect.line.fill.background()
        r, g, b = colors.header
        r2 = min(r + 40, 255)
        g2 = min(g + 40, 255)
        b2 = min(b + 40, 255)
        sp_pr = bg_rect._element.find(qn("p:spPr"))
        if sp_pr is None:
            sp_pr = bg_rect._element.find(qn("a:spPr"))
        if sp_pr is not None:
            for child in list(sp_pr):
                tag_local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                if tag_local in ("solidFill", "gradFill", "noFill"):
                    sp_pr.remove(child)
            grad_xml = (
                f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                f'<a:gsLst>'
                f'<a:gs pos="0"><a:srgbClr val="{r:02X}{g:02X}{b:02X}"/></a:gs>'
                f'<a:gs pos="100000"><a:srgbClr val="{r2:02X}{g2:02X}{b2:02X}"/></a:gs>'
                f'</a:gsLst>'
                f'<a:lin ang="5400000" scaled="1"/>'
                f'</a:gradFill>'
            )
            sp_pr.append(etree.fromstring(grad_xml))
        sp = bg_rect._element
        sp.getparent().remove(sp)
        slide.shapes._spTree.insert(2, sp)
    except Exception:
        _set_pptx_slide_background(slide, colors.header)

    # Centered title text box
    title_box = slide.shapes.add_textbox(
        Inches(1.5), Inches(2.0), Inches(10.3), Inches(2.5),
    )
    title_box.text_frame.word_wrap = True
    title_box.text_frame.text = slide_data.title
    for paragraph in title_box.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.color.rgb = _rgb_color(colors.title)
            run.font.bold = True
            run.font.size = Pt(44)

    # Accent line (centered below title area)
    try:
        accent_line = slide.shapes.add_shape(
            1, Inches(3.3), Inches(4.6), Inches(6.7), Inches(0.04),
        )
        accent_line.fill.solid()
        accent_line.fill.fore_color.rgb = _rgb_color(colors.accent)
        accent_line.line.fill.background()
    except Exception:
        pass

    # Subtitle (first content item, below accent line)
    if slide_data.content:
        sub_box = slide.shapes.add_textbox(
            Inches(2.0), Inches(4.9), Inches(9.3), Inches(1.0),
        )
        sub_box.text_frame.word_wrap = True
        sub_box.text_frame.text = slide_data.content[0]
        for paragraph in sub_box.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(22)
                run.font.color.rgb = _rgb_color(colors.accent)

    if slide_data.speaker_notes:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


def _add_section_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors, slide_index: int = 0):
    """Add an enhanced section divider slide with gradient background, accent bar, large title, and faded section number."""
    slide_layout = prs.slide_layouts[5]  # blank layout for full control
    slide = prs.slides.add_slide(slide_layout)

    # Full-slide gradient background (header -> lighter shade)
    try:
        from lxml import etree
        bg_rect = slide.shapes.add_shape(
            1, Inches(0), Inches(0), Inches(13.333), Inches(7.5),
        )
        bg_rect.line.fill.background()
        r, g, b = colors.header
        r2 = min(r + 50, 255)
        g2 = min(g + 50, 255)
        b2 = min(b + 50, 255)
        sp_pr = bg_rect._element.find(qn("p:spPr"))
        if sp_pr is None:
            sp_pr = bg_rect._element.find(qn("a:spPr"))
        if sp_pr is not None:
            for child in list(sp_pr):
                tag_local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                if tag_local in ("solidFill", "gradFill", "noFill"):
                    sp_pr.remove(child)
            grad_xml = (
                f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                f'<a:gsLst>'
                f'<a:gs pos="0"><a:srgbClr val="{r:02X}{g:02X}{b:02X}"/></a:gs>'
                f'<a:gs pos="100000"><a:srgbClr val="{r2:02X}{g2:02X}{b2:02X}"/></a:gs>'
                f'</a:gsLst>'
                f'<a:lin ang="5400000" scaled="1"/>'
                f'</a:gradFill>'
            )
            sp_pr.append(etree.fromstring(grad_xml))
        # Move background to back
        sp = bg_rect._element
        sp.getparent().remove(sp)
        slide.shapes._spTree.insert(2, sp)
    except Exception:
        _set_pptx_slide_background(slide, colors.header)

    # Left accent bar shape
    try:
        accent_bar = slide.shapes.add_shape(
            1, Inches(0), Inches(0), Inches(0.12), Inches(7.5),
        )
        accent_bar.fill.solid()
        accent_bar.fill.fore_color.rgb = _rgb_color(colors.accent)
        accent_bar.line.fill.background()
    except Exception:
        pass

    # Large faded section number overlay (right side, behind title)
    try:
        from lxml import etree
        section_num = str(slide_index + 1)
        num_box = slide.shapes.add_textbox(
            Inches(7.5), Inches(0.5), Inches(5.5), Inches(6.5),
        )
        num_box.text_frame.word_wrap = False
        num_box.text_frame.text = section_num
        for paragraph in num_box.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.RIGHT
            for run in paragraph.runs:
                run.font.bold = True
                run.font.size = Pt(280)
                run.font.color.rgb = _rgb_color(colors.accent)
        # Set 20% opacity on the text via OpenXML solidFill alpha
        for run_elem in num_box.text_frame._txBody.findall(f".//{qn('a:solidFill')}"):
            clr = run_elem.find(qn("a:srgbClr"))
            if clr is not None:
                alpha_elem = etree.SubElement(clr, qn("a:alpha"))
                alpha_elem.set("val", "20000")  # 20% opacity
    except Exception:
        pass

    # Large centered title text box
    title_box = slide.shapes.add_textbox(
        Inches(1.0), Inches(2.5), Inches(11.3), Inches(2.0),
    )
    title_box.text_frame.word_wrap = True
    title_box.text_frame.text = slide_data.title
    for paragraph in title_box.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.color.rgb = _rgb_color(colors.title)
            run.font.bold = True
            run.font.size = Pt(54)

    # Accent underline shape (centered below title)
    try:
        line_shape = slide.shapes.add_shape(
            1, Inches(4.0), Inches(4.7), Inches(5.0), Inches(0.06),
        )
        line_shape.fill.solid()
        line_shape.fill.fore_color.rgb = _rgb_color(colors.accent)
        line_shape.line.fill.background()
    except Exception:
        pass

    if slide_data.speaker_notes:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


def _add_two_column_slide(prs: Presentation, slide_data: SlideData, colors: ThemeColors):
    """Add a two-column layout slide with header bar, dual text boxes and divider."""
    slide_layout = prs.slide_layouts[5]  # blank layout
    slide = prs.slides.add_slide(slide_layout)

    _set_pptx_slide_background(slide, colors.background)

    # Header bar for visual parity with image renderer
    _add_pptx_header_bar(slide, colors)

    # Title text box
    from pptx.util import Inches, Pt, Emu
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3), Inches(12.3), Inches(1.0),
    )
    title_box.text_frame.word_wrap = True
    title_box.text_frame.text = slide_data.title
    for paragraph in title_box.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb = _rgb_color(colors.title)
            run.font.bold = True
            run.font.size = Pt(32)

    # Vertical divider line
    try:
        divider = slide.shapes.add_shape(
            1,  # MSO_SHAPE.RECTANGLE
            Inches(6.55), Inches(1.6), Inches(0.03), Inches(5.0),
        )
        divider.fill.solid()
        divider.fill.fore_color.rgb = _rgb_color(colors.accent)
        divider.line.fill.background()
    except Exception:
        pass

    # Split content into two columns
    content = slide_data.content
    mid = max(1, len(content) // 2)
    left_items = content[:mid]
    right_items = content[mid:]

    # Responsive font size based on total content density
    col_font_size = _compute_pptx_font_size(content, base_size=16, min_size=11)

    # Left column text box
    left_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(1.6), Inches(5.9), Inches(5.0),
    )
    left_box.text_frame.word_wrap = True
    _populate_pptx_bullets(left_box.text_frame, left_items, colors, col_font_size)

    # Right column text box
    right_box = slide.shapes.add_textbox(
        Inches(6.8), Inches(1.6), Inches(5.9), Inches(5.0),
    )
    right_box.text_frame.word_wrap = True
    _populate_pptx_bullets(right_box.text_frame, right_items, colors, col_font_size)

    if slide_data.speaker_notes:
        slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes


# ---- Pillow Slide Image Renderers ----

def _draw_header_gradient(img: Image.Image, colors: ThemeColors):
    """Draw a gradient header bar from header color to a slightly lighter shade."""
    r, g, b = colors.header
    lighter = (min(r + 30, 255), min(g + 30, 255), min(b + 30, 255))
    _draw_gradient_rect(img, (0, 0, SLIDE_WIDTH, HEADER_HEIGHT), colors.header, lighter)


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


def _draw_slide_footer(
    draw: ImageDraw.Draw,
    footer_font: ImageFont.FreeTypeFont,
    colors: ThemeColors,
    slide_index: int,
    total_slides: int,
    has_bg_image: bool = False,
    shadow: bool = False,
    footer_company: str = "",
    footer_author: str = "",
):
    """Draw the footer area with slide number and optional branding."""
    footer_color = (200, 200, 200) if has_bg_image else colors.footer

    # Right: slide number
    footer_text = f"Slide {slide_index + 1} / {total_slides}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_w = bbox[2] - bbox[0]
    _draw_text(
        draw, (SLIDE_WIDTH - footer_w - 50, SLIDE_HEIGHT - 45),
        footer_text, footer_font, footer_color, shadow=shadow,
    )

    # Left: company branding
    if footer_company:
        _draw_text(
            draw, (MARGIN_X, SLIDE_HEIGHT - 45),
            footer_company, footer_font, footer_color, shadow=shadow,
        )

    # Center: author
    if footer_author:
        bbox_a = draw.textbbox((0, 0), footer_author, font=footer_font)
        author_w = bbox_a[2] - bbox_a[0]
        _draw_text(
            draw, ((SLIDE_WIDTH - author_w) // 2, SLIDE_HEIGHT - 45),
            footer_author, footer_font, footer_color, shadow=shadow,
        )


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
    footer_company: str = "",
    footer_author: str = "",
):
    """Render a title/cover slide with centered content."""
    shadow = has_bg_image

    if not has_bg_image:
        # Gradient background for title slide
        _draw_gradient_rect(draw._image, (0, 0, SLIDE_WIDTH, SLIDE_HEIGHT), colors.header,
                            (min(colors.header[0] + 40, 255), min(colors.header[1] + 40, 255), min(colors.header[2] + 40, 255)))

    # Accent line
    accent_y = SLIDE_HEIGHT // 2 + 40
    draw.rectangle([(SLIDE_WIDTH // 4, accent_y), (3 * SLIDE_WIDTH // 4, accent_y + 4)], fill=colors.accent)

    # Centered title with wrapping
    title_color = (255, 255, 255) if has_bg_image else colors.title
    title_max_w = SLIDE_WIDTH - 2 * MARGIN_X
    title_lines, used_font = _fit_title_in_header(
        slide_data.title, title_font, language, title_max_w,
    )
    if len(title_lines) == 1:
        bbox = draw.textbbox((0, 0), title_lines[0], font=used_font)
        title_w = bbox[2] - bbox[0]
        title_h = bbox[3] - bbox[1]
        title_x = (SLIDE_WIDTH - title_w) // 2
        title_y = SLIDE_HEIGHT // 2 - title_h - 30
        _draw_text(draw, (title_x, title_y), title_lines[0], used_font, title_color, shadow=shadow)
    else:
        bbox0 = draw.textbbox((0, 0), title_lines[0], font=used_font)
        line_h = bbox0[3] - bbox0[1]
        total_h = line_h * len(title_lines) + 10 * (len(title_lines) - 1)
        start_y = SLIDE_HEIGHT // 2 - total_h - 10
        for li, tl in enumerate(title_lines):
            bbox = draw.textbbox((0, 0), tl, font=used_font)
            w = bbox[2] - bbox[0]
            x = (SLIDE_WIDTH - w) // 2
            _draw_text(draw, (x, start_y + li * (line_h + 10)), tl, used_font, title_color, shadow=shadow)

    # Subtitle (first content item)
    if slide_data.content:
        subtitle = slide_data.content[0]
        bbox = draw.textbbox((0, 0), subtitle, font=content_font)
        sub_w = bbox[2] - bbox[0]
        sub_x = (SLIDE_WIDTH - sub_w) // 2
        _draw_text(draw, (sub_x, accent_y + 30), subtitle, content_font, colors.accent, shadow=shadow)

    # Footer
    _draw_slide_footer(draw, footer_font, colors, slide_index, total_slides, has_bg_image, shadow,
                      footer_company=footer_company, footer_author=footer_author)


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
    footer_company: str = "",
    footer_author: str = "",
):
    """Render a section divider slide with gradient background and accent styling."""
    shadow = has_bg_image

    if not has_bg_image:
        # Full-slide gradient from header color to slightly lighter
        r, g, b = colors.header
        lighter = (min(r + 50, 255), min(g + 50, 255), min(b + 50, 255))
        _draw_gradient_rect(draw._image, (0, 0, SLIDE_WIDTH, SLIDE_HEIGHT), colors.header, lighter)

    # Left accent bar (wider than before)
    draw.rectangle([(0, 0), (12, SLIDE_HEIGHT)], fill=colors.accent)

    # Large section number in faded accent behind title
    section_num_font = _get_font("DejaVuSans-Bold.ttf", 200, language)
    section_num = str(slide_index + 1)
    bbox_num = draw.textbbox((0, 0), section_num, font=section_num_font)
    num_w = bbox_num[2] - bbox_num[0]
    # Faded number at right side
    faded_color = (*colors.accent, 60) if has_bg_image else (
        min(colors.header[0] + 20, 255),
        min(colors.header[1] + 20, 255),
        min(colors.header[2] + 20, 255),
    )
    _draw_text(draw, (SLIDE_WIDTH - num_w - 80, SLIDE_HEIGHT // 2 - 120), section_num,
               section_num_font, faded_color, shadow=False)

    # Centered large title
    title = slide_data.title
    large_font = _get_font("DejaVuSans-Bold.ttf", 90, language)
    bbox = draw.textbbox((0, 0), title, font=large_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    title_x = (SLIDE_WIDTH - title_w) // 2
    title_y = (SLIDE_HEIGHT - title_h) // 2 - 20
    title_color = (255, 255, 255) if has_bg_image else colors.title
    _draw_text(draw, (title_x, title_y), title, large_font, title_color, shadow=shadow)

    # Accent underline
    line_y = title_y + title_h + 25
    line_w = min(title_w + 60, 700)
    line_x = (SLIDE_WIDTH - line_w) // 2
    draw.rectangle([(line_x, line_y), (line_x + line_w, line_y + 5)], fill=colors.accent)

    # Footer
    _draw_slide_footer(draw, footer_font, colors, slide_index, total_slides, has_bg_image, shadow,
                      footer_company=footer_company, footer_author=footer_author)


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
    footer_company: str = "",
    footer_author: str = "",
):
    """Render a two-column content slide."""
    shadow = has_bg_image

    # Gradient header bar
    _draw_header_gradient(draw._image, colors)
    _draw_decorative_elements(draw, colors, slide_index, total_slides)

    # Title with wrapping
    title_lines, used_title_font = _fit_title_in_header(
        slide_data.title, title_font, language, CONTENT_MAX_WIDTH,
    )
    if len(title_lines) == 1:
        bbox = draw.textbbox((0, 0), title_lines[0], font=used_title_font)
        title_h = bbox[3] - bbox[1]
        title_y = (HEADER_HEIGHT - title_h) // 2
        _draw_text(draw, (MARGIN_X, title_y), title_lines[0], used_title_font, colors.title, shadow=False)
    else:
        bbox0 = draw.textbbox((0, 0), title_lines[0], font=used_title_font)
        line_h = bbox0[3] - bbox0[1]
        total_h = line_h * len(title_lines) + 8 * (len(title_lines) - 1)
        start_y = (HEADER_HEIGHT - total_h) // 2
        for li, line in enumerate(title_lines):
            _draw_text(draw, (MARGIN_X, start_y + li * (line_h + 8)), line, used_title_font, colors.title, shadow=False)

    # Vertical divider line
    mid_x = SLIDE_WIDTH // 2
    divider_color = (200, 200, 200) if has_bg_image else colors.footer
    draw.rectangle([(mid_x - 1, CONTENT_START_Y), (mid_x + 1, SLIDE_HEIGHT - 80)], fill=divider_color)

    # Split content into two columns
    content = slide_data.content
    mid = max(1, len(content) // 2)
    left_items = content[:mid]
    right_items = content[mid:]

    # Responsive font sizing for columns
    available_h = SLIDE_HEIGHT - CONTENT_START_Y - FOOTER_AREA
    all_items = max(len(left_items), len(right_items))
    longest_col = left_items if len(left_items) >= len(right_items) else right_items
    font_size = _compute_content_font_size(
        longest_col, language, COLUMN_MAX_WIDTH, available_h,
    )
    if font_size < CONTENT_FONT_SIZE:
        content_font = _get_font("DejaVuSans.ttf", font_size, language)
    line_spacing = int(font_size * 1.67)

    for col_idx, (items, start_x) in enumerate([(left_items, MARGIN_X), (right_items, mid_x + 40)]):
        y = CONTENT_START_Y
        max_y = SLIDE_HEIGHT - FOOTER_AREA
        overflow = False
        for bi, point in enumerate(items):
            if y >= max_y:
                overflow = True
                break
            wrapped = _wrap_text(point, content_font, COLUMN_MAX_WIDTH)
            bullet_icon = _BULLET_ICONS[bi % len(_BULLET_ICONS)]
            for j, line in enumerate(wrapped):
                if y + line_spacing > max_y:
                    # Truncate last visible line with ellipsis
                    trunc = line[:40] + "\u2026" if len(line) > 40 else line + "\u2026"
                    if j == 0:
                        _draw_text(draw, (start_x, y), bullet_icon, content_font, colors.accent, shadow=shadow)
                        bullet_w = _text_pixel_width(bullet_icon + " ", content_font)
                        _draw_text(draw, (start_x + bullet_w, y), trunc, content_font, colors.text, shadow=shadow)
                    else:
                        _draw_text(draw, (start_x, y), f"  {trunc}", content_font, colors.text, shadow=shadow)
                    overflow = True
                    break
                if j == 0:
                    _draw_text(draw, (start_x, y), bullet_icon, content_font, colors.accent, shadow=shadow)
                    bullet_w = _text_pixel_width(bullet_icon + " ", content_font)
                    _draw_text(draw, (start_x + bullet_w, y), line, content_font, colors.text, shadow=shadow)
                else:
                    _draw_text(draw, (start_x, y), f"  {line}", content_font, colors.text, shadow=shadow)
                y += line_spacing
            if overflow:
                break
            y += 10
        if overflow:
            logger.debug("Two-column col %d overflowed at slide %d", col_idx, slide_index)

    # Footer with branding
    _draw_slide_footer(draw, footer_font, colors, slide_index, total_slides, has_bg_image, shadow,
                      footer_company=footer_company, footer_author=footer_author)


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
    footer_company: str = "",
    footer_author: str = "",
):
    """Render a standard content slide with responsive font sizing."""
    shadow = has_bg_image

    # Gradient header bar
    _draw_header_gradient(draw._image, colors)
    _draw_decorative_elements(draw, colors, slide_index, total_slides)

    # Title with wrapping for long titles
    title_lines, used_title_font = _fit_title_in_header(
        slide_data.title, title_font, language, CONTENT_MAX_WIDTH,
    )
    if len(title_lines) == 1:
        bbox = draw.textbbox((0, 0), title_lines[0], font=used_title_font)
        title_h = bbox[3] - bbox[1]
        title_y = (HEADER_HEIGHT - title_h) // 2
        _draw_text(draw, (MARGIN_X, title_y), title_lines[0], used_title_font, colors.title, shadow=False)
    else:
        bbox0 = draw.textbbox((0, 0), title_lines[0], font=used_title_font)
        line_h = bbox0[3] - bbox0[1]
        total_h = line_h * len(title_lines) + 8 * (len(title_lines) - 1)
        start_y = (HEADER_HEIGHT - total_h) // 2
        for li, line in enumerate(title_lines):
            _draw_text(draw, (MARGIN_X, start_y + li * (line_h + 8)), line, used_title_font, colors.title, shadow=False)

    # Responsive font sizing: shrink font if content won't fit
    available_h = SLIDE_HEIGHT - CONTENT_START_Y - FOOTER_AREA
    font_size = _compute_content_font_size(
        slide_data.content, language, CONTENT_MAX_WIDTH, available_h,
    )
    if font_size < CONTENT_FONT_SIZE:
        content_font = _get_font("DejaVuSans.ttf", font_size, language)
    line_spacing = int(font_size * 1.67)

    # Content with CJK-aware wrapping and themed bullets (with overflow ellipsis)
    y = CONTENT_START_Y
    max_y = SLIDE_HEIGHT - FOOTER_AREA
    overflow = False
    for bi, point in enumerate(slide_data.content):
        if y >= max_y:
            overflow = True
            break
        wrapped = _wrap_text(point, content_font, CONTENT_MAX_WIDTH)
        bullet_icon = _BULLET_ICONS[bi % len(_BULLET_ICONS)]
        for j, line in enumerate(wrapped):
            if y + line_spacing > max_y:
                # Truncate last visible line with ellipsis
                trunc = line[:40] + "\u2026" if len(line) > 40 else line + "\u2026"
                if j == 0:
                    _draw_text(draw, (MARGIN_X, y), bullet_icon, content_font, colors.accent, shadow=shadow)
                    bullet_w = _text_pixel_width(bullet_icon + " ", content_font)
                    _draw_text(draw, (MARGIN_X + bullet_w, y), trunc, content_font, colors.text, shadow=shadow)
                else:
                    x = MARGIN_X + BULLET_INDENT
                    _draw_text(draw, (x, y), f"  {trunc}", content_font, colors.text, shadow=shadow)
                overflow = True
                break
            if j == 0:
                # Draw accent-colored bullet icon
                _draw_text(draw, (MARGIN_X, y), bullet_icon, content_font, colors.accent, shadow=shadow)
                bullet_w = _text_pixel_width(bullet_icon + " ", content_font)
                _draw_text(draw, (MARGIN_X + bullet_w, y), line, content_font, colors.text, shadow=shadow)
            else:
                x = MARGIN_X + BULLET_INDENT
                _draw_text(draw, (x, y), f"  {line}", content_font, colors.text, shadow=shadow)
            y += line_spacing
        if overflow:
            break
        y += 10
    if overflow:
        logger.debug("Content overflowed at slide %d", slide_index)

    # Footer with branding
    _draw_slide_footer(draw, footer_font, colors, slide_index, total_slides, has_bg_image, shadow,
                      footer_company=footer_company, footer_author=footer_author)


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
    overlay_opacity: int = BG_OVERLAY_OPACITY,
    footer_company: str = "",
    footer_author: str = "",
) -> List[str]:
    """
    Render high-quality slide images using Pillow.
    Supports themes, layouts, AI background images, CJK fonts, text shadows,
    responsive font sizing, and footer branding.
    """
    os.makedirs(output_dir, exist_ok=True)
    colors = THEMES.get(theme, THEMES[SlideTheme.PROFESSIONAL])
    image_paths = []

    title_font = _get_font("DejaVuSans-Bold.ttf", TITLE_FONT_SIZE, language)
    content_font = _get_font("DejaVuSans.ttf", CONTENT_FONT_SIZE, language)
    footer_font = _get_font("DejaVuSans.ttf", FOOTER_FONT_SIZE, language)

    total_slides = len(slides_data)

    for i, slide_data in enumerate(slides_data):
        img = _prepare_background(i, colors, background_images, overlay_opacity=overlay_opacity)
        draw = ImageDraw.Draw(img)

        has_bg = background_images is not None and i in background_images
        renderer = _LAYOUT_RENDERERS.get(slide_data.layout, _render_content_layout)
        renderer(
            draw, slide_data, colors, title_font, content_font, footer_font,
            i, total_slides, has_bg_image=has_bg, language=language,
            footer_company=footer_company, footer_author=footer_author,
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


def create_pdf_from_images(
    image_paths: List[str],
    output_path: str,
    title: str = "",
    author: str = "",
) -> str:
    """Compile slide images into a single PDF document with optional metadata."""
    if not image_paths:
        raise ValueError("No images provided for PDF generation")

    images = [Image.open(p).convert("RGB") for p in image_paths]

    # Build save kwargs
    save_kwargs = {
        "save_all": True,
        "append_images": images[1:],
        "resolution": 300,
    }

    # Add PDF metadata if Pillow supports it
    if title or author:
        try:
            from PIL import PdfImagePlugin
            info = PdfImagePlugin.PdfInfo()
            if title:
                info.title = title
            if author:
                info.author = author
            info.creator = "AutoPresentation AI"
            save_kwargs["append_images"] = images[1:]
            images[0].save(output_path, **save_kwargs)
        except (ImportError, AttributeError, Exception):
            # Fallback: save without metadata if PdfInfo not available
            images[0].save(output_path, **save_kwargs)
    else:
        images[0].save(output_path, **save_kwargs)

    logger.info("PDF saved: %s (%d pages)", output_path, len(images))
    return output_path
