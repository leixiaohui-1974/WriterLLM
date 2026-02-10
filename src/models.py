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


@dataclass
class SlideData:
    """Represents a single slide's content."""
    title: str
    content: List[str] = field(default_factory=list)
    speaker_notes: str = ""
    image_prompt: str = ""

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "speaker_notes": self.speaker_notes,
            "image_prompt": self.image_prompt,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SlideData":
        return cls(
            title=data.get("title", "Untitled"),
            content=data.get("content", []),
            speaker_notes=data.get("speaker_notes", ""),
            image_prompt=data.get("image_prompt", ""),
        )


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
        background=(250, 250, 250),
        header=(250, 250, 250),
        text=(60, 60, 60),
        title=(30, 30, 30),
        accent=(100, 100, 100),
        footer=(180, 180, 180),
    ),
}
