from PIL import Image

img = Image.open("test_output/images/slide_001.png")
width, height = img.size

# Crop content area: y > 300
content_area = img.crop((0, 300, width, height))
pixels = list(content_area.getdata())

# Count non-white pixels
# Background is (255, 255, 255)
non_white = [p for p in pixels if p != (255, 255, 255)]
print(f"Non-white pixels in content area: {len(non_white)}")

# Count text color pixels (approx (50, 50, 50))
text_pixels = [p for p in pixels if 40 <= p[0] <= 60 and 40 <= p[1] <= 60 and 40 <= p[2] <= 60]
print(f"Text pixels count: {len(text_pixels)}")

# Also check Footer (grey)
footer_area = img.crop((0, height-60, width, height))
footer_pixels = list(footer_area.getdata())
footer_grey = [p for p in footer_pixels if 140 <= p[0] <= 160] # (150, 150, 150)
print(f"Footer pixels count: {len(footer_grey)}")

if len(text_pixels) > 100:
    print("Content Text CONFIRMED")
else:
    print("Content Text MISSING")
