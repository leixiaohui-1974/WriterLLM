from PIL import ImageFont, ImageDraw, Image
import os

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(font_path):
    print("WARNING: Expected font path not found!")
    # Check fallback logic
    import glob
    fonts = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
    if fonts:
        print(f"Found fallback font: {fonts[0]}")
    else:
        print("WARNING: No fonts found in /usr/share/fonts! Using PIL default.")

        # Create a sample image with default font to see how small it is
        img = Image.new('RGB', (1920, 1080), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.load_default()
            draw.text((100, 100), "This is the default font at 1920x1080", font=font, fill=(0,0,0))
            # Check bounding box
            bbox = font.getbbox("This is the default font at 1920x1080")
            print(f"Default font bbox height: {bbox[3] - bbox[1]}")
        except Exception as e:
            print(f"Error loading default font: {e}")
else:
    print(f"Font found at {font_path}")
