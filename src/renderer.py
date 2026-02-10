from pptx import Presentation
from pptx.util import Inches, Pt
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

def create_pptx_file(slides_data, output_path):
    """
    Creates a PowerPoint file from the slide data.
    """
    prs = Presentation()

    for slide_data in slides_data:
        # Layout 1 is 'Title and Content'
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)

        # Title
        if slide.shapes.title:
            slide.shapes.title.text = slide_data.get("title", "Untitled Slide")

        # Content
        if len(slide.placeholders) > 1:
            content_placeholder = slide.placeholders[1]
            if content_placeholder.has_text_frame:
                tf = content_placeholder.text_frame
                content_list = slide_data.get("content", [])

                if content_list:
                    tf.text = content_list[0]
                    for point in content_list[1:]:
                        p = tf.add_paragraph()
                        p.text = point

        # Speaker Notes
        if slide.has_notes_slide:
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = slide_data.get("speaker_notes", "")

    prs.save(output_path)
    return output_path

def create_slide_images(slides_data, output_dir):
    """
    Generates images for each slide using Pillow.
    Returns a list of image paths.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_paths = []

    width = 1920
    height = 1080
    background_color = (255, 255, 255)
    header_color = (70, 130, 180) # Steel Blue
    text_color = (0, 0, 0)

    # Font Logic
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font_path):
        # Fallback search
        import glob
        fonts = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
        if fonts:
            font_path = fonts[0]
        else:
            font_path = None

    try:
        if font_path:
            title_font = ImageFont.truetype(font_path, 60)
            content_font = ImageFont.truetype(font_path, 40)
            footer_font = ImageFont.truetype(font_path, 30)
        else:
            # Load default bitmap font
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            footer_font = ImageFont.load_default()
    except Exception as e:
        print(f"Font loading warning: {e}")
        title_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    for i, slide_data in enumerate(slides_data):
        img = Image.new('RGB', (width, height), color=background_color)
        draw = ImageDraw.Draw(img)

        # Draw header
        draw.rectangle([(0, 0), (width, 150)], fill=header_color)

        # Title
        title = slide_data.get("title", "Untitled")
        draw.text((50, 45), title, font=title_font, fill=(255, 255, 255))

        # Content
        y_text = 250
        content_lines = slide_data.get("content", [])

        # Basic text wrapping
        max_chars = 60
        for point in content_lines:
            # Use textwrap to split long lines
            wrapped_lines = textwrap.wrap(point, width=max_chars)
            for line in wrapped_lines:
                draw.text((100, y_text), f"• {line}", font=content_font, fill=text_color)
                y_text += 60 # Line spacing

        # Footer
        draw.text((width - 200, height - 50), f"Slide {i+1}", font=footer_font, fill=(100, 100, 100))

        image_filename = f"slide_{i+1:03d}.png"
        image_path = os.path.join(output_dir, image_filename)
        img.save(image_path)
        image_paths.append(image_path)

    return image_paths

def create_pdf_from_images(image_paths, output_path):
    """
    Compiles a list of images into a single PDF.
    """
    if not image_paths:
        return None

    images = [Image.open(p).convert('RGB') for p in image_paths]

    # Save first image and append the rest
    first_image = images[0]
    first_image.save(
        output_path,
        save_all=True,
        append_images=images[1:]
    )
    return output_path
