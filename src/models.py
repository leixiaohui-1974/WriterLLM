"""
Data models for the AutoPresentation AI pipeline.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class SlideTheme(Enum):
    """Available slide visual themes."""
    PROFESSIONAL = "professional"
    DARK = "dark"
    OCEAN = "ocean"
    SUNSET = "sunset"
    MINIMAL = "minimal"
    FOREST = "forest"
    ROYAL = "royal"
    TECH = "tech"


class SlideLayout(Enum):
    """Slide layout types for varied visual presentation."""
    TITLE = "title"          # Title slide with centered text
    CONTENT = "content"      # Standard bullet-point content
    SECTION = "section"      # Section divider with large title
    TWO_COLUMN = "two_column"  # Two-column layout


class Language(Enum):
    """Supported languages for TTS and content generation."""
    ENGLISH = "en"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    FRENCH = "fr"
    GERMAN = "de"
    SPANISH = "es"


# Voice mappings: (language, gender) -> edge-tts voice name
VOICE_MAP = {
    (Language.ENGLISH, "Male"): "en-US-ChristopherNeural",
    (Language.ENGLISH, "Female"): "en-US-JennyNeural",
    (Language.CHINESE, "Male"): "zh-CN-YunxiNeural",
    (Language.CHINESE, "Female"): "zh-CN-XiaoxiaoNeural",
    (Language.JAPANESE, "Male"): "ja-JP-KeitaNeural",
    (Language.JAPANESE, "Female"): "ja-JP-NanamiNeural",
    (Language.KOREAN, "Male"): "ko-KR-InJoonNeural",
    (Language.KOREAN, "Female"): "ko-KR-SunHiNeural",
    (Language.FRENCH, "Male"): "fr-FR-HenriNeural",
    (Language.FRENCH, "Female"): "fr-FR-DeniseNeural",
    (Language.GERMAN, "Male"): "de-DE-ConradNeural",
    (Language.GERMAN, "Female"): "de-DE-KatjaNeural",
    (Language.SPANISH, "Male"): "es-ES-AlvaroNeural",
    (Language.SPANISH, "Female"): "es-ES-ElviraNeural",
}


SLIDE_TEMPLATES = {
    "blank": {
        "label": "Blank",
        "title": "New Slide",
        "content": ["New content point"],
        "notes": "Speaker notes here.",
        "layout": SlideLayout.CONTENT,
    },
    "intro": {
        "label": "Introduction",
        "title": "Introduction",
        "content": ["Background and context", "Key objectives", "Scope of this presentation"],
        "notes": "Welcome the audience and provide an overview of the presentation.",
        "layout": SlideLayout.CONTENT,
    },
    "comparison": {
        "label": "Comparison",
        "title": "Comparison",
        "content": ["Option A: advantage 1", "Option A: advantage 2", "Option B: advantage 1", "Option B: advantage 2"],
        "notes": "Compare and contrast the two options, highlighting trade-offs.",
        "layout": SlideLayout.TWO_COLUMN,
    },
    "section_break": {
        "label": "Section Break",
        "title": "Section Title",
        "content": [],
        "notes": "Transition to the next section of the presentation.",
        "layout": SlideLayout.SECTION,
    },
    "key_points": {
        "label": "Key Points",
        "title": "Key Takeaways",
        "content": ["First key insight or finding", "Second important conclusion", "Third actionable recommendation"],
        "notes": "Summarize the most important points for the audience.",
        "layout": SlideLayout.CONTENT,
    },
    "thank_you": {
        "label": "Thank You",
        "title": "Thank You",
        "content": ["Questions and discussion"],
        "notes": "Thank the audience and open the floor for questions.",
        "layout": SlideLayout.TITLE,
    },
}


@dataclass
class SlideData:
    """Represents a single slide's content."""
    title: str
    content: List[str] = field(default_factory=list)
    speaker_notes: str = ""
    image_prompt: str = ""
    layout: SlideLayout = SlideLayout.CONTENT
    duration_override: Optional[float] = None  # Min seconds for video (None = auto)

    def to_dict(self) -> dict:
        d = {
            "title": self.title,
            "content": self.content,
            "speaker_notes": self.speaker_notes,
            "image_prompt": self.image_prompt,
            "layout": self.layout.value,
        }
        if self.duration_override is not None:
            d["duration_override"] = self.duration_override
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "SlideData":
        layout_str = data.get("layout", "content")
        try:
            layout = SlideLayout(layout_str)
        except ValueError:
            layout = SlideLayout.CONTENT
        dur = data.get("duration_override")
        return cls(
            title=data.get("title", "Untitled"),
            content=data.get("content", []),
            speaker_notes=data.get("speaker_notes", ""),
            image_prompt=data.get("image_prompt", ""),
            layout=layout,
            duration_override=float(dur) if dur is not None else None,
        )


class ExportFormat(Enum):
    """Available export formats."""
    PPTX = "pptx"
    PDF = "pdf"
    VIDEO = "video"


@dataclass
class PresentationConfig:
    """Configuration for presentation generation."""
    num_slides: int = 5
    language: Language = Language.ENGLISH
    voice_gender: str = "Female"
    theme: SlideTheme = SlideTheme.PROFESSIONAL
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    custom_prompt: str = ""
    overlay_opacity: int = 130  # 0=transparent, 255=opaque
    speaking_rate: str = "+0%"  # TTS speaking rate: "+20%", "-10%", etc.
    footer_company: str = ""  # Company or branding text shown in footer left
    footer_author: str = ""   # Author name shown in footer center
    enable_animations: bool = True  # Bullet-by-bullet entrance animations in PPTX
    transition_duration_ms: int = 700  # Slide transition duration in milliseconds
    transition_type: str = "fade"  # Slide transition type (fade, push, wipe, cover, split, dissolve)
    export_formats: List[ExportFormat] = field(
        default_factory=lambda: [ExportFormat.PPTX, ExportFormat.PDF, ExportFormat.VIDEO]
    )

    @property
    def voice_name(self) -> str:
        """Get the edge-tts voice name based on language and gender."""
        key = (self.language, self.voice_gender)
        return VOICE_MAP.get(key, "en-US-JennyNeural")


@dataclass
class ThemeColors:
    """Color scheme for a slide theme."""
    background: tuple
    header: tuple
    text: tuple
    title: tuple
    accent: tuple
    footer: tuple


# Theme definitions
THEMES = {
    SlideTheme.PROFESSIONAL: ThemeColors(
        background=(255, 255, 255),
        header=(44, 62, 80),
        text=(50, 50, 50),
        title=(255, 255, 255),
        accent=(52, 152, 219),
        footer=(150, 150, 150),
    ),
    SlideTheme.DARK: ThemeColors(
        background=(30, 30, 30),
        header=(20, 20, 20),
        text=(220, 220, 220),
        title=(255, 255, 255),
        accent=(46, 204, 113),
        footer=(100, 100, 100),
    ),
    SlideTheme.OCEAN: ThemeColors(
        background=(236, 240, 241),
        header=(41, 128, 185),
        text=(44, 62, 80),
        title=(255, 255, 255),
        accent=(26, 188, 156),
        footer=(127, 140, 141),
    ),
    SlideTheme.SUNSET: ThemeColors(
        background=(255, 248, 240),
        header=(192, 57, 43),
        text=(60, 40, 30),
        title=(255, 255, 255),
        accent=(243, 156, 18),
        footer=(160, 140, 130),
    ),
    SlideTheme.MINIMAL: ThemeColors(
        background=(248, 248, 248),
        header=(235, 235, 235),
        text=(50, 50, 50),
        title=(30, 30, 30),
        accent=(80, 80, 80),
        footer=(170, 170, 170),
    ),
    SlideTheme.FOREST: ThemeColors(
        background=(245, 248, 243),
        header=(39, 78, 19),
        text=(45, 55, 40),
        title=(255, 255, 255),
        accent=(76, 175, 80),
        footer=(140, 160, 130),
    ),
    SlideTheme.ROYAL: ThemeColors(
        background=(240, 238, 248),
        header=(63, 25, 118),
        text=(50, 40, 70),
        title=(255, 255, 255),
        accent=(156, 39, 176),
        footer=(140, 130, 160),
    ),
    SlideTheme.TECH: ThemeColors(
        background=(18, 18, 28),
        header=(10, 10, 20),
        text=(200, 210, 220),
        title=(255, 255, 255),
        accent=(0, 188, 212),
        footer=(80, 90, 100),
    ),
}

# Max upload file size (50 MB)
MAX_UPLOAD_SIZE_MB = 50
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024


def serialize_project(slides: List[SlideData], language: str = "en",
                      theme: str = "professional", **kwargs) -> dict:
    """Serialize slides and settings to a JSON-compatible dict for project save."""
    return {
        "version": "24.0",
        "settings": {
            "language": language,
            "theme": theme,
            **kwargs,
        },
        "slides": [s.to_dict() for s in slides],
    }


def deserialize_project(data: dict) -> tuple:
    """
    Deserialize a project dict back to slides and settings.
    Returns (slides: List[SlideData], settings: dict).
    """
    slides = [SlideData.from_dict(s) for s in data.get("slides", [])]
    settings = data.get("settings", {})
    return slides, settings
