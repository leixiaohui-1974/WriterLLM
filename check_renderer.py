from src.renderer import create_slide_images
import os

data = [{
    "title": "Slide with Many Lines",
    "content": [
        "First point is short.",
        "Second point is very long and will wrap because it has many words to verify the wrapping logic. " * 3,
        "Third point.",
        "Fourth point.",
        "Fifth point.",
        "Sixth point.",
        "Seventh point.",
        "Eighth point.",
        "Ninth point.",
        "Tenth point.",
        "Eleventh point.",
        "Twelfth point.",
        "Thirteenth point.",
        "Fourteenth point.",
        "Fifteenth point.",
        "Sixteenth point."
    ],
    "speaker_notes": "Note 1"
}]

os.makedirs("test_render_output", exist_ok=True)
paths = create_slide_images(data, "test_render_output")
print(f"Created {paths[0]}")

# Check image size
from PIL import Image
img = Image.open(paths[0])
print(f"Image Size: {img.size}")
# Check if bottom right pixel is white (background) or overwritten
pixel = img.getpixel((1919, 1079))
print(f"Bottom Right Pixel: {pixel}")
