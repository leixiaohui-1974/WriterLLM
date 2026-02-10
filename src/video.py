"""
Video generation module - creates presentation videos with TTS voiceovers.
Supports multiple languages and improved error handling.
"""
import asyncio
import logging
import os
import shutil
from typing import List, Optional

import edge_tts
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

from src.config import VIDEO_FPS, DEFAULT_SLIDE_DURATION, AUDIO_PADDING, MIN_AUDIO_SIZE

logger = logging.getLogger(__name__)


async def _generate_audio_async(text: str, output_path: str, voice: str) -> bool:
    """Generate TTS audio asynchronously. Returns True on success."""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return True
    except Exception as e:
        logger.error("Edge TTS error (voice=%s): %s", voice, e)
        return False


def generate_voiceover(text: str, output_path: str, voice: str = "en-US-JennyNeural") -> Optional[str]:
    """
    Generate a TTS audio file from text.
    Returns the output path on success, None on failure.
    """
    if not text or not text.strip():
        logger.debug("Empty text, skipping TTS generation")
        return None

    try:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("closed loop")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        success = loop.run_until_complete(_generate_audio_async(text, output_path, voice))

        if success and os.path.exists(output_path) and os.path.getsize(output_path) > MIN_AUDIO_SIZE:
            return output_path

        logger.warning("TTS output missing or too small: %s", output_path)
        return None

    except Exception as e:
        logger.error("TTS generation failed: %s", e)
        return None


def create_video_presentation(
    image_paths: List[str],
    text_scripts: List[str],
    output_path: str,
    voice: str = "en-US-JennyNeural",
    progress_callback=None,
) -> Optional[str]:
    """
    Create a video presentation from slide images and text scripts.

    Args:
        image_paths: List of slide image file paths.
        text_scripts: List of speaker notes for each slide.
        output_path: Where to save the output MP4.
        voice: Edge TTS voice name.
        progress_callback: Optional callable(current, total) for progress updates.

    Returns:
        Output path on success, None on failure.
    """
    if not image_paths:
        logger.error("No images provided for video generation")
        return None

    clips = []
    temp_audio_dir = os.path.join(os.path.dirname(os.path.abspath(output_path)), "temp_audio")
    os.makedirs(temp_audio_dir, exist_ok=True)

    total = len(image_paths)
    logger.info("Creating video from %d slides (voice: %s)", total, voice)

    try:
        for i, img_path in enumerate(image_paths):
            script = text_scripts[i] if i < len(text_scripts) else ""

            if progress_callback:
                progress_callback(i, total)

            audio_path = os.path.join(temp_audio_dir, f"audio_{i:03d}.mp3")
            generated_audio = generate_voiceover(script, audio_path, voice)

            if generated_audio:
                try:
                    audio_clip = AudioFileClip(generated_audio)
                    duration = audio_clip.duration + AUDIO_PADDING
                    img_clip = ImageClip(img_path).with_duration(duration).with_audio(audio_clip)
                    clips.append(img_clip)
                    logger.debug("Slide %d: %.1fs with audio", i + 1, duration)
                except Exception as e:
                    logger.warning("Slide %d: audio clip error (%s), using default duration", i + 1, e)
                    clips.append(ImageClip(img_path).with_duration(DEFAULT_SLIDE_DURATION))
            else:
                logger.info("Slide %d: no audio, using default %ss duration", i + 1, DEFAULT_SLIDE_DURATION)
                clips.append(ImageClip(img_path).with_duration(DEFAULT_SLIDE_DURATION))

        if not clips:
            logger.error("No video clips created")
            return None

        if progress_callback:
            progress_callback(total, total)

        logger.info("Encoding video...")
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(
            output_path,
            fps=VIDEO_FPS,
            codec="libx264",
            audio_codec="aac",
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            logger=None,
        )

        logger.info("Video saved: %s (%.1fs)", output_path, final_video.duration)
        return output_path

    except Exception as e:
        logger.error("Video generation failed: %s", e)
        raise

    finally:
        if os.path.exists(temp_audio_dir):
            try:
                shutil.rmtree(temp_audio_dir)
            except OSError as e:
                logger.debug("Could not clean temp audio dir: %s", e)
