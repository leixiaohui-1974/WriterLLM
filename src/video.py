"""
Video generation module - creates presentation videos with TTS voiceovers.
Supports multiple languages, fade transitions, TTS retry logic,
and improved error handling.
"""
import asyncio
import logging
import os
import shutil
import time
from typing import List, Optional

from src.config import (
    VIDEO_FPS, DEFAULT_SLIDE_DURATION, AUDIO_PADDING, MIN_AUDIO_SIZE,
    CROSSFADE_DURATION,
)

# Lazy imports for heavy dependencies (edge_tts, moviepy)
# These are imported inside functions so the module can be imported without them.
edge_tts = None
ImageClip = None
AudioFileClip = None
concatenate_videoclips = None
vfx = None


def _ensure_deps():
    """Lazily import edge_tts and moviepy on first use."""
    global edge_tts, ImageClip, AudioFileClip, concatenate_videoclips, vfx
    if edge_tts is None:
        import edge_tts as _edge_tts
        edge_tts = _edge_tts
    if ImageClip is None:
        from moviepy import ImageClip as _IC, AudioFileClip as _AFC, concatenate_videoclips as _cv, vfx as _vfx
        ImageClip = _IC
        AudioFileClip = _AFC
        concatenate_videoclips = _cv
        vfx = _vfx

logger = logging.getLogger(__name__)

# TTS retry settings
_TTS_MAX_RETRIES = 3


async def _generate_audio_async(text: str, output_path: str, voice: str, rate: str = "+0%") -> bool:
    """Generate TTS audio asynchronously. Returns True on success."""
    try:
        _ensure_deps()
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_path)
        return True
    except Exception as e:
        logger.error("Edge TTS error (voice=%s, rate=%s): %s", voice, rate, e)
        return False


def generate_voiceover(
    text: str, output_path: str, voice: str = "en-US-JennyNeural", rate: str = "+0%",
) -> Optional[str]:
    """
    Generate a TTS audio file from text with retry logic and speaking rate control.
    Returns the output path on success, None on failure.
    """
    if not text or not text.strip():
        logger.debug("Empty text, skipping TTS generation")
        return None

    for attempt in range(_TTS_MAX_RETRIES):
        try:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    raise RuntimeError("closed loop")
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            success = loop.run_until_complete(_generate_audio_async(text, output_path, voice, rate))

            if success and os.path.exists(output_path) and os.path.getsize(output_path) > MIN_AUDIO_SIZE:
                return output_path

            logger.warning("TTS attempt %d: output missing or too small", attempt + 1)

        except Exception as e:
            logger.warning("TTS attempt %d failed: %s", attempt + 1, e)

        if attempt < _TTS_MAX_RETRIES - 1:
            wait = 2 ** attempt
            logger.info("Retrying TTS in %ds...", wait)
            time.sleep(wait)

    logger.error("All %d TTS attempts failed for: %s...", _TTS_MAX_RETRIES, text[:50])
    return None


def _apply_fade_effects(clip, index: int, total: int, fade_duration: float = CROSSFADE_DURATION):
    """Apply fade-in/fade-out transitions to a video clip."""
    _ensure_deps()
    effects = []
    # Fade in for first clip, fade out for last clip, both for middle clips
    if index == 0:
        effects.append(vfx.FadeIn(fade_duration))
    elif index == total - 1:
        effects.append(vfx.FadeOut(fade_duration))
    else:
        effects.append(vfx.FadeIn(fade_duration))
        effects.append(vfx.FadeOut(fade_duration))

    if effects:
        return clip.with_effects(effects)
    return clip


def _format_srt_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt_subtitles(
    text_scripts: List[str],
    slide_durations: List[float],
    output_path: str,
) -> Optional[str]:
    """
    Generate an SRT subtitle file from slide scripts and durations.

    Args:
        text_scripts: Speaker notes for each slide.
        slide_durations: Duration in seconds for each slide.
        output_path: Where to save the .srt file.

    Returns:
        Output path on success, None on failure.
    """
    if not text_scripts or not slide_durations:
        return None

    try:
        entries = []
        current_time = 0.0
        for i, (script, duration) in enumerate(zip(text_scripts, slide_durations)):
            text = script.strip() if script else ""
            if not text:
                current_time += duration
                continue

            start = current_time
            end = current_time + duration
            entries.append(
                f"{len(entries) + 1}\n"
                f"{_format_srt_timestamp(start)} --> {_format_srt_timestamp(end)}\n"
                f"{text}\n"
            )
            current_time = end

        if not entries:
            return None

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(entries))

        logger.info("SRT subtitles saved: %s (%d entries)", output_path, len(entries))
        return output_path

    except Exception as e:
        logger.error("SRT generation failed: %s", e)
        return None


def create_video_presentation(
    image_paths: List[str],
    text_scripts: List[str],
    output_path: str,
    voice: str = "en-US-JennyNeural",
    progress_callback=None,
    enable_transitions: bool = True,
    speaking_rate: str = "+0%",
    generate_subtitles: bool = True,
    duration_overrides: Optional[List[Optional[float]]] = None,
) -> Optional[str]:
    """
    Create a video presentation from slide images and text scripts.

    Args:
        image_paths: List of slide image file paths.
        text_scripts: List of speaker notes for each slide.
        output_path: Where to save the output MP4.
        voice: Edge TTS voice name.
        progress_callback: Optional callable(current, total) for progress updates.
        enable_transitions: Whether to add fade transitions between slides.
        speaking_rate: TTS speaking rate (e.g., "+0%", "+20%", "-10%").
        generate_subtitles: Whether to generate an SRT subtitle file alongside the video.
        duration_overrides: Optional list of minimum durations (seconds) per slide.

    Returns:
        Output path on success, None on failure.
    """
    if not image_paths:
        logger.error("No images provided for video generation")
        return None

    temp_audio_dir = os.path.join(os.path.dirname(os.path.abspath(output_path)), "temp_audio")
    clips = []
    final_video = None

    try:
        _ensure_deps()

        slide_durations = []
        os.makedirs(temp_audio_dir, exist_ok=True)

        total = len(image_paths)
        logger.info("Creating video from %d slides (voice: %s, rate: %s, transitions: %s)", total, voice, speaking_rate, enable_transitions)
        for i, img_path in enumerate(image_paths):
            script = text_scripts[i] if i < len(text_scripts) else ""

            if progress_callback:
                progress_callback(i, total)

            # Validate image file exists before processing
            if not os.path.exists(img_path):
                logger.warning("Slide %d: image not found (%s), skipping", i + 1, img_path)
                continue

            audio_path = os.path.join(temp_audio_dir, f"audio_{i:03d}.mp3")
            generated_audio = generate_voiceover(script, audio_path, voice, rate=speaking_rate)

            # Per-slide minimum duration override
            min_dur = None
            if duration_overrides and i < len(duration_overrides):
                min_dur = duration_overrides[i]

            if generated_audio:
                try:
                    audio_clip = AudioFileClip(generated_audio)
                    duration = audio_clip.duration + AUDIO_PADDING
                    # Apply minimum duration override
                    if min_dur is not None and min_dur > duration:
                        duration = min_dur
                    img_clip = ImageClip(img_path).with_duration(duration).with_audio(audio_clip)
                    clips.append(img_clip)
                    slide_durations.append(duration)
                    logger.debug("Slide %d: %.1fs with audio", i + 1, duration)
                except Exception as e:
                    logger.warning("Slide %d: audio clip error (%s), using default duration", i + 1, e)
                    fallback = max(DEFAULT_SLIDE_DURATION, min_dur or 0)
                    clips.append(ImageClip(img_path).with_duration(fallback))
                    slide_durations.append(fallback)
            else:
                fallback = max(DEFAULT_SLIDE_DURATION, min_dur or 0)
                logger.info("Slide %d: no audio, using %.1fs duration", i + 1, fallback)
                clips.append(ImageClip(img_path).with_duration(fallback))
                slide_durations.append(fallback)

        if not clips:
            logger.error("No video clips created")
            return None

        # Generate SRT subtitles
        if generate_subtitles and slide_durations:
            srt_path = os.path.splitext(output_path)[0] + ".srt"
            generate_srt_subtitles(text_scripts, slide_durations, srt_path)

        # Apply fade transitions
        if enable_transitions and len(clips) > 1:
            clips = [_apply_fade_effects(clip, i, len(clips)) for i, clip in enumerate(clips)]

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
        return None

    finally:
        # Clean up moviepy clip resources to release file handles
        for _clip in clips:
            try:
                _clip.close()
            except Exception:
                pass
        if final_video is not None:
            try:
                final_video.close()
            except Exception:
                pass
        if os.path.exists(temp_audio_dir):
            try:
                shutil.rmtree(temp_audio_dir)
            except OSError as e:
                logger.debug("Could not clean temp audio dir: %s", e)
