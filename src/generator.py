"""
AI content generation module - transforms extracted text into structured slide data.
Supports OpenAI-compatible APIs with retry logic and multi-language prompts.
"""
import json
import logging
import time
from typing import List, Optional

from src.models import SlideData, Language

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
    logger.warning("openai package not installed; LLM generation unavailable.")


# Language-specific system prompts
SYSTEM_PROMPTS = {
    Language.ENGLISH: "You are a professional presentation assistant. You output structured JSON.",
    Language.CHINESE: "你是一个专业的演示文稿助手。你输出结构化的JSON格式内容。",
    Language.JAPANESE: "あなたはプロのプレゼンテーションアシスタントです。構造化されたJSONを出力します。",
    Language.KOREAN: "당신은 전문 프레젠테이션 어시스턴트입니다. 구조화된 JSON을 출력합니다.",
    Language.FRENCH: "Vous êtes un assistant de présentation professionnel. Vous produisez du JSON structuré.",
    Language.GERMAN: "Sie sind ein professioneller Präsentationsassistent. Sie geben strukturiertes JSON aus.",
    Language.SPANISH: "Eres un asistente de presentaciones profesional. Produces JSON estructurado.",
}


def _build_prompt(text: str, num_slides: int, language: Language, max_input_length: int = 6000) -> str:
    """Build the LLM prompt for slide generation."""
    truncated = text[:max_input_length]
    if len(text) > max_input_length:
        truncated += "\n\n[... text truncated ...]"

    lang_instructions = {
        Language.ENGLISH: f"""Analyze the following text and create a {num_slides}-slide presentation.
Return a JSON object with a key "slides" containing an array of slide objects.
Each slide object must have:
- "title": string (concise slide title)
- "content": list of strings (3-5 bullet points per slide)
- "speaker_notes": string (2-3 sentences of natural presenter script)
- "image_prompt": string (visual description for the slide background)

Requirements:
- The first slide should be a title/introduction slide
- The last slide should be a summary/conclusion slide
- Bullet points should be concise (under 80 characters each)
- Speaker notes should be conversational and natural""",
        Language.CHINESE: f"""分析以下文本，创建一个{num_slides}页的演示文稿。
返回一个JSON对象，包含键"slides"，其值为幻灯片对象数组。
每个幻灯片对象必须包含：
- "title": 字符串（简洁的幻灯片标题）
- "content": 字符串列表（每页3-5个要点）
- "speaker_notes": 字符串（2-3句自然的演讲稿）
- "image_prompt": 字符串（幻灯片背景的视觉描述，用英文）

要求：
- 第一页应该是标题/引言页
- 最后一页应该是总结/结论页
- 要点应简洁（每条不超过40个字符）
- 演讲稿应自然流畅""",
    }

    instruction = lang_instructions.get(language, lang_instructions[Language.ENGLISH])
    return f"{instruction}\n\nText to analyze:\n{truncated}"


def _validate_slides(slides_data: list, num_slides: int) -> List[SlideData]:
    """Validate and normalize slide data from LLM response."""
    validated = []
    for i, item in enumerate(slides_data):
        if not isinstance(item, dict):
            logger.warning("Slide %d is not a dict, skipping", i)
            continue

        title = str(item.get("title", f"Slide {i + 1}")).strip()
        if len(title) < 2:
            title = f"Slide {i + 1}"

        content = item.get("content", [])
        if isinstance(content, str):
            content = [content]
        content = [str(c).strip() for c in content if c]

        speaker_notes = str(item.get("speaker_notes", "")).strip()
        image_prompt = str(item.get("image_prompt", "")).strip()

        validated.append(SlideData(
            title=title,
            content=content if content else [""],
            speaker_notes=speaker_notes,
            image_prompt=image_prompt,
        ))

    if not validated:
        raise ValueError("No valid slides produced from LLM response")

    return validated


def mock_generate_content(text: str, num_slides: int, language: Language = Language.ENGLISH) -> List[SlideData]:
    """
    Generate slide content without an LLM by splitting text intelligently.
    Used as fallback or for testing without API keys.
    """
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n") if line.strip()]
    sentences = []
    for line in lines:
        for sep in ["\u3002", ".", "!", "\uff1f", "?"]:
            line = line.replace(sep, sep + "||SPLIT||")
        parts = [s.strip() for s in line.split("||SPLIT||") if s.strip()]
        sentences.extend(parts)

    if not sentences:
        sentences = ["Content placeholder"] * (num_slides * 3)

    slides = []
    chunk_size = max(1, len(sentences) // num_slides)

    for i in range(num_slides):
        start = i * chunk_size
        end = min(len(sentences), start + chunk_size)

        if start >= len(sentences):
            start = max(0, len(sentences) - chunk_size)
            end = len(sentences)

        chunk = sentences[start:end] if sentences[start:end] else ["Content placeholder"]

        title = chunk[0][:60] if len(chunk[0]) >= 5 else f"Slide {i + 1}"
        content = chunk[1:6] if len(chunk) > 1 else [chunk[0]]
        notes = " ".join(chunk)[:300]

        slides.append(SlideData(
            title=title,
            content=content,
            speaker_notes=notes,
            image_prompt=f"Professional presentation slide about: {title}",
        ))

    return slides


def llm_generate_content(
    text: str,
    api_key: str,
    base_url: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    num_slides: int = 5,
    language: Language = Language.ENGLISH,
    max_retries: int = 3,
) -> List[SlideData]:
    """
    Use an OpenAI-compatible LLM to generate structured slide content.
    Includes retry logic with exponential backoff.
    """
    if not OpenAI:
        raise ImportError("openai package not installed. Run: pip install openai")

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url
    client = OpenAI(**client_kwargs)

    prompt = _build_prompt(text, num_slides, language)
    system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS[Language.ENGLISH])

    last_error = None
    for attempt in range(max_retries):
        try:
            logger.info("LLM request attempt %d/%d (model: %s)", attempt + 1, max_retries, model)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            content = response.choices[0].message.content
            data = json.loads(content)

            slides_raw = None
            if "slides" in data:
                slides_raw = data["slides"]
            elif isinstance(data, list):
                slides_raw = data
            else:
                for v in data.values():
                    if isinstance(v, list) and len(v) > 0:
                        slides_raw = v
                        break

            if slides_raw is None:
                raise ValueError("LLM response does not contain a slides array")

            slides = _validate_slides(slides_raw, num_slides)
            logger.info("Successfully generated %d slides via LLM", len(slides))
            return slides

        except json.JSONDecodeError as e:
            last_error = e
            logger.warning("Attempt %d: JSON parse error: %s", attempt + 1, e)
        except Exception as e:
            last_error = e
            logger.warning("Attempt %d: LLM error: %s", attempt + 1, e)

        if attempt < max_retries - 1:
            wait = 2 ** attempt
            logger.info("Retrying in %ds...", wait)
            time.sleep(wait)

    logger.error("All %d LLM attempts failed. Last error: %s", max_retries, last_error)
    logger.info("Falling back to mock content generation")
    return mock_generate_content(text, num_slides, language)


def generate_slides(
    text: str,
    num_slides: int = 5,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    language: Language = Language.ENGLISH,
) -> List[SlideData]:
    """
    Main entry point for content generation.
    Uses LLM if API key is provided, otherwise falls back to mock mode.
    """
    if api_key:
        return llm_generate_content(text, api_key, base_url, model, num_slides, language)
    else:
        logger.info("No API key provided, using mock content generation")
        return mock_generate_content(text, num_slides, language)
