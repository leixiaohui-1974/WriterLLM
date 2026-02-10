import asyncio
import edge_tts
from moviepy import AudioFileClip

async def create_audio():
    communicate = edge_tts.Communicate("Hello", "en-US-ChristopherNeural")
    await communicate.save("test.mp3")

asyncio.run(create_audio())

try:
    clip = AudioFileClip("test.mp3")
    print(f"Audio duration: {clip.duration}")
except Exception as e:
    print(f"Error: {e}")
