"""
AI image generation module for slide backgrounds.
Supports OpenAI DALL-E and compatible image generation APIs.
"""
import logging
import os
import base64
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import requests
except ImportError:
    requests = None


def generate_slide_image(
    prompt: str,
    output_path: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = "dall-e-3",
    size: str = "1792x1024",
) -> Optional[str]:
    """
    Generate an AI image for a slide using an image generation API.

    Args:
        prompt: Description of the image to generate.
        output_path: Where to save the generated image.
        api_key: API key for the image generation service.
        base_url: Base URL for API-compatible endpoints.
        model: Model name (e.g., "dall-e-3", "dall-e-2").
        size: Image size (e.g., "1792x1024", "1024x1024").

    Returns:
        Output path on success, None on failure.
    """
    if not api_key:
        logger.debug("No API key for image generation, skipping")
        return None

    if not OpenAI:
        logger.warning("openai package not available for image generation")
        return None

    # Enhance prompt for presentation context
    enhanced_prompt = (
        f"Professional presentation slide background image. "
        f"Clean, modern, high-quality. No text or words in the image. "
        f"Subject: {prompt}"
    )

    try:
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        client = OpenAI(**client_kwargs)

        logger.info("Generating image (model: %s, size: %s)", model, size)
        response = client.images.generate(
            model=model,
            prompt=enhanced_prompt,
            size=size,
            quality="standard",
            n=1,
            response_format="b64_json",
        )

        image_data = base64.b64decode(response.data[0].b64_json)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_data)

        logger.info("Image generated: %s", output_path)
        return output_path

    except Exception as e:
        logger.warning("Image generation failed: %s", e)
        return None


def generate_slide_images_batch(
    prompts: list,
    output_dir: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = "dall-e-3",
    progress_callback=None,
) -> dict:
    """
    Generate AI images for multiple slides.

    Args:
        prompts: List of (index, prompt) tuples.
        output_dir: Directory to save generated images.
        api_key: API key for image generation.
        base_url: Optional API base URL.
        model: Image generation model name.
        progress_callback: Optional callable(current, total).

    Returns:
        Dict mapping slide index to generated image path.
    """
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    total = len(prompts)

    for i, (slide_idx, prompt) in enumerate(prompts):
        if progress_callback:
            progress_callback(i, total)

        output_path = os.path.join(output_dir, f"bg_{slide_idx:03d}.png")
        result = generate_slide_image(
            prompt, output_path,
            api_key=api_key, base_url=base_url, model=model,
        )
        if result:
            results[slide_idx] = result

    if progress_callback:
        progress_callback(total, total)

    logger.info("Generated %d/%d slide images", len(results), total)
    return results
