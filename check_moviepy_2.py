from PIL import Image
from moviepy import ImageClip

img = Image.new('RGB', (100, 100), color=(255, 0, 0))
img.save("test.png")

try:
    clip = ImageClip("test.png")
    print(f"ImageClip created successfully. Duration method: {hasattr(clip, 'with_duration')}")
    if hasattr(clip, 'with_duration'):
        clip = clip.with_duration(5)
    else:
        clip = clip.set_duration(5)
    print("Duration set.")
except Exception as e:
    print(f"Error: {e}")
