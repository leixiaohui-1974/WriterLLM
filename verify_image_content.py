from PIL import Image
import os

img_path = "test_output/images/slide_001.png"
if not os.path.exists(img_path):
    print("Image not found")
    exit(1)

img = Image.open(img_path)
print(f"Image size: {img.size}")
# Check pixel colors to ensure it's not all white
pixels = list(img.getdata())
unique_pixels = set(pixels)
print(f"Unique pixel colors count: {len(unique_pixels)}")

# Check header color (approx)
header_pixel = img.getpixel((100, 50))
print(f"Header pixel at (100, 50): {header_pixel}")

# Check content pixel (should be text color)
# Text starts at margin 100, y=300. Let's sample around there.
# Since we don't know exact text position, we just check if there are dark pixels
dark_pixels = [p for p in pixels if sum(p) < 100]
print(f"Dark pixels count: {len(dark_pixels)}")

if len(dark_pixels) > 1000:
    print("Text likely present.")
else:
    print("WARNING: Image might be empty.")
