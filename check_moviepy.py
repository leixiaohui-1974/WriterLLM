from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import os

print("Imports successful")
try:
    # Check if ImageClip accepts simple string path
    clip = ImageClip("test.png")
except Exception as e:
    print(f"ImageClip error: {e}")
