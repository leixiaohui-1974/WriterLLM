"""
Configuration management for AutoPresentation AI.
Supports environment variables and .env files.
"""
import os
import logging

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Configure application-wide logging."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_env(key: str, default: str = "") -> str:
    """Get an environment variable with fallback."""
    return os.environ.get(key, default)


# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.debug(".env file loaded")
except ImportError:
    pass


# Application defaults from environment
DEFAULT_API_KEY = get_env("OPENAI_API_KEY")
DEFAULT_BASE_URL = get_env("OPENAI_BASE_URL")
DEFAULT_MODEL = get_env("OPENAI_MODEL", "gpt-3.5-turbo")

# Slide image dimensions
SLIDE_WIDTH = 1920
SLIDE_HEIGHT = 1080

# Font sizes
TITLE_FONT_SIZE = 70
CONTENT_FONT_SIZE = 45
FOOTER_FONT_SIZE = 30

# Video settings
VIDEO_FPS = 24
DEFAULT_SLIDE_DURATION = 5.0
AUDIO_PADDING = 0.5
MIN_AUDIO_SIZE = 1024  # bytes
CROSSFADE_DURATION = 0.4  # seconds for fade transitions between slides

# Background image overlay opacity (0=transparent, 255=opaque)
# Controls how much the theme overlay covers the AI background image
BG_OVERLAY_OPACITY = 130

# Text processing
MAX_LLM_INPUT_LENGTH = 6000
TEXT_WRAP_WIDTH = 70
