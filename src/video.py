import asyncio
import edge_tts
import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

async def _generate_audio_async(text, output_path, voice):
    """
    Async helper to generate TTS audio.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_voiceover(text, output_path, voice="en-US-ChristopherNeural"):
    """
    Generates an audio file from text using edge-tts.
    Synchronous wrapper for async function.
    """
    if not text or not text.strip():
        # Create a silence file (0.5s) using moviepy logic later, but for now just pass empty
        return None

    try:
        asyncio.run(_generate_audio_async(text, output_path, voice))
        if os.path.exists(output_path):
            return output_path
        return None
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

def create_video_presentation(image_paths, text_scripts, output_path, voice="en-US-ChristopherNeural"):
    """
    Creates a video from a list of images and corresponding text scripts.
    """
    clips = []
    temp_audio_files = []

    # Ensure output directory for audio exists
    audio_dir = os.path.join(os.path.dirname(os.path.abspath(output_path)), "temp_audio")
    os.makedirs(audio_dir, exist_ok=True)

    for i, (img_path, script) in enumerate(zip(image_paths, text_scripts)):
        # Generate Audio
        audio_filename = f"audio_{i}.mp3"
        audio_path = os.path.join(audio_dir, audio_filename)

        generated_audio = generate_voiceover(script, audio_path, voice)

        if generated_audio:
            temp_audio_files.append(generated_audio)

            # Create Audio Clip
            audio_clip = AudioFileClip(generated_audio)
            duration = audio_clip.duration + 0.5 # Add 0.5s padding

            # Create Image Clip
            img_clip = ImageClip(img_path).with_duration(duration)
            img_clip = img_clip.with_audio(audio_clip)

            clips.append(img_clip)
        else:
            # Fallback for failed/empty audio: just show slide for 5 seconds
            img_clip = ImageClip(img_path).with_duration(5)
            clips.append(img_clip)

    if not clips:
        return None

    # Concatenate
    final_video = concatenate_videoclips(clips, method="compose")

    # Write file
    # Use 'libx264' codec and 'aac' audio for compatibility
    try:
        final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    except Exception as e:
        print(f"Video writing error: {e}")
        # Try fallback codec if needed, but libx264 is standard
        raise e

    # Cleanup temp audio
    for audio_file in temp_audio_files:
        try:
            os.remove(audio_file)
        except:
            pass
    try:
        os.rmdir(audio_dir)
    except:
        pass

    return output_path
