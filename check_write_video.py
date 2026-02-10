from moviepy import ImageClip, concatenate_videoclips
from PIL import Image
import os

img = Image.new('RGB', (100, 100), color=(0, 255, 0))
img.save("test_video.png")

clip = ImageClip("test_video.png").with_duration(1)
final = concatenate_videoclips([clip])
final.write_videofile("test.mp4", fps=24, codec="libx264")
print("Video written.")
