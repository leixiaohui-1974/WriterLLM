"""
AI content generation module - transforms extracted text into structured slide data.
Supports OpenAI-compatible APIs with retry logic, multi-language prompts, and layout assignment.
"""
import json
import logging
import time
from typing import List, Optional

from src.models import SlideData, SlideLayout, Language

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
    logger.warning("openai package not installed; LLM generation unavailable.")


# Language-specific system prompts
SYSTEM_PROMPTS = {
    Language.ENGLISH: "You are a professional presentation designer. You output structured JSON.",
    Language.CHINESE: "你是一个专业的演示文稿设计师。你输出结构化的JSON格式内容。",
    Language.JAPANESE: "あなたはプロのプレゼンテーションデザイナーです。構造化されたJSONを出力します。",
    Language.KOREAN: "당신은 전문 프레젠테이션 디자이너입니다. 구조화된 JSON을 출력합니다.",
    Language.FRENCH: "Vous \u00eates un concepteur de pr\u00e9sentations professionnel. Vous produisez du JSON structur\u00e9.",
    Language.GERMAN: "Sie sind ein professioneller Pr\u00e4sentationsdesigner. Sie geben strukturiertes JSON aus.",
    Language.SPANISH: "Eres un dise\u00f1ador de presentaciones profesional. Produces JSON estructurado.",
}

# Full language-specific prompts
_PROMPT_TEMPLATES = {
    Language.ENGLISH: """Analyze the following text and create a {num_slides}-slide presentation.
Return a JSON object with a key "slides" containing an array of slide objects.
Each slide object must have:
- "title": string (concise slide title)
- "content": list of strings (3-5 bullet points per slide)
- "speaker_notes": string (2-3 sentences of natural presenter script)
- "image_prompt": string (detailed visual description for AI image generation, in English)
- "layout": string (one of: "title", "content", "section", "two_column")

Layout rules:
- The first slide MUST use "title" layout
- Use "section" layout for topic transitions (1-2 per presentation)
- Use "two_column" for comparison or pros/cons slides (if appropriate)
- Use "content" for all other slides
- The last slide should be a summary/conclusion

Requirements:
- Bullet points should be concise (under 80 characters each)
- Speaker notes should be conversational and natural
- Image prompts should describe a professional, relevant visual scene""",

    Language.CHINESE: """分析以下文本，创建一个{num_slides}页的演示文稿。
返回一个JSON对象，包含键"slides"，其值为幻灯片对象数组。
每个幻灯片对象必须包含：
- "title": 字符串（简洁的幻灯片标题）
- "content": 字符串列表（每页3-5个要点）
- "speaker_notes": 字符串（2-3句自然的演讲稿）
- "image_prompt": 字符串（AI图像生成的详细视觉描述，用英文）
- "layout": 字符串（可选值："title", "content", "section", "two_column"）

布局规则：
- 第一页必须使用"title"布局
- 话题过渡使用"section"布局（每个演示文稿1-2个）
- 对比或优缺点使用"two_column"布局
- 其他页面使用"content"布局
- 最后一页应该是总结/结论

要求：
- 要点应简洁（每条不超过40个字符）
- 演讲稿应自然流畅
- 图像提示应描述专业、相关的视觉场景（用英文）""",

    Language.JAPANESE: """以下のテキストを分析し、{num_slides}ページのプレゼンテーションを作成してください。
"slides"キーを含むJSONオブジェクトを返してください。
各スライドオブジェクトには以下を含める必要があります：
- "title": 文字列（簡潔なスライドタイトル）
- "content": 文字列のリスト（各スライド3-5の箇条書き）
- "speaker_notes": 文字列（2-3文の自然なプレゼンタースクリプト）
- "image_prompt": 文字列（AI画像生成の詳細な視覚的説明、英語で）
- "layout": 文字列（"title", "content", "section", "two_column"のいずれか）

レイアウトルール：
- 最初のスライドは"title"レイアウトを使用
- トピックの移行には"section"を使用
- 比較には"two_column"を使用
- その他は"content"を使用""",

    Language.KOREAN: """다음 텍스트를 분석하여 {num_slides}페이지 프레젠테이션을 만들어 주세요.
"slides" 키를 포함하는 JSON 객체를 반환하세요.
각 슬라이드 객체에는 다음이 포함되어야 합니다:
- "title": 문자열 (간결한 슬라이드 제목)
- "content": 문자열 목록 (슬라이드당 3-5개의 요점)
- "speaker_notes": 문자열 (자연스러운 발표자 대본 2-3문장)
- "image_prompt": 문자열 (AI 이미지 생성을 위한 상세 시각적 설명, 영어로)
- "layout": 문자열 ("title", "content", "section", "two_column" 중 하나)""",

    Language.FRENCH: """Analysez le texte suivant et cr\u00e9ez une pr\u00e9sentation de {num_slides} diapositives.
Retournez un objet JSON avec une cl\u00e9 "slides" contenant un tableau d'objets.
Chaque objet doit avoir :
- "title": cha\u00eene (titre concis)
- "content": liste de cha\u00eenes (3-5 points par diapositive)
- "speaker_notes": cha\u00eene (2-3 phrases naturelles)
- "image_prompt": cha\u00eene (description visuelle d\u00e9taill\u00e9e en anglais)
- "layout": cha\u00eene ("title", "content", "section", "two_column")""",

    Language.GERMAN: """Analysieren Sie den folgenden Text und erstellen Sie eine {num_slides}-Folien-Pr\u00e4sentation.
Geben Sie ein JSON-Objekt mit dem Schl\u00fcssel "slides" zur\u00fcck.
Jedes Folienobjekt muss enthalten:
- "title": String (pr\u00e4gnanter Folientitel)
- "content": Liste von Strings (3-5 Aufz\u00e4hlungspunkte pro Folie)
- "speaker_notes": String (2-3 nat\u00fcrliche S\u00e4tze)
- "image_prompt": String (detaillierte visuelle Beschreibung auf Englisch)
- "layout": String ("title", "content", "section", "two_column")""",

    Language.SPANISH: """Analiza el siguiente texto y crea una presentaci\u00f3n de {num_slides} diapositivas.
Devuelve un objeto JSON con la clave "slides" que contenga un array de objetos.
Cada objeto debe tener:
- "title": cadena (t\u00edtulo conciso)
- "content": lista de cadenas (3-5 vi\u00f1etas por diapositiva)
- "speaker_notes": cadena (2-3 oraciones naturales)
- "image_prompt": cadena (descripci\u00f3n visual detallada en ingl\u00e9s)
- "layout": cadena ("title", "content", "section", "two_column")""",
}


def _build_prompt(text: str, num_slides: int, language: Language,
                  max_input_length: int = 6000, custom_prompt: str = "") -> str:
    """Build the LLM prompt for slide generation."""
    truncated = text[:max_input_length]
    if len(text) > max_input_length:
        truncated += "\n\n[... text truncated ...]"

    template = _PROMPT_TEMPLATES.get(language, _PROMPT_TEMPLATES[Language.ENGLISH])
    instruction = template.format(num_slides=num_slides)

    if custom_prompt:
        instruction += f"\n\nAdditional instructions: {custom_prompt}"

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

        layout_str = item.get("layout", "content")
        try:
            layout = SlideLayout(layout_str)
        except ValueError:
            layout = SlideLayout.CONTENT

        validated.append(SlideData(
            title=title,
            content=content if content else [""],
            speaker_notes=speaker_notes,
            image_prompt=image_prompt,
            layout=layout,
        ))

    if not validated:
        raise ValueError("No valid slides produced from LLM response")

    return validated


_TOC_TITLES = {
    Language.ENGLISH: "Agenda",
    Language.CHINESE: "\u76ee\u5f55",
    Language.JAPANESE: "\u30a2\u30b8\u30a7\u30f3\u30c0",
    Language.KOREAN: "\ubaa9\ucc28",
    Language.FRENCH: "Sommaire",
    Language.GERMAN: "Agenda",
    Language.SPANISH: "Agenda",
}


def _create_toc_slide(slides: List[SlideData], language: Language) -> SlideData:
    """Create a table of contents / agenda slide from slide titles."""
    toc_title = _TOC_TITLES.get(language, "Agenda")
    # Collect titles from content slides (skip title and summary)
    toc_items = []
    for s in slides:
        if s.layout not in (SlideLayout.TITLE,) and s.title:
            toc_items.append(s.title[:60])
    if not toc_items:
        toc_items = ["Overview"]
    return SlideData(
        title=toc_title,
        content=toc_items[:8],
        speaker_notes=f"Here is our agenda for today's presentation.",
        image_prompt="Professional agenda slide, clean table of contents, modern design",
        layout=SlideLayout.CONTENT,
    )


def _assign_layouts(slides: List[SlideData]) -> List[SlideData]:
    """Assign smart layouts to slides generated by mock mode."""
    if not slides:
        return slides

    # First slide = title
    slides[0].layout = SlideLayout.TITLE

    # Last slide = content (summary)
    if len(slides) > 1:
        slides[-1].layout = SlideLayout.CONTENT

    # Middle slides: assign section dividers periodically
    if len(slides) > 4:
        section_interval = max(3, len(slides) // 3)
        for i in range(1, len(slides) - 1):
            if i % section_interval == 0:
                slides[i].layout = SlideLayout.SECTION

    # Assign two_column to slides with 6+ bullet points
    for slide in slides:
        if slide.layout == SlideLayout.CONTENT and len(slide.content) >= 6:
            slide.layout = SlideLayout.TWO_COLUMN

    return slides


_TRANSITION_PHRASES = {
    Language.ENGLISH: [
        "Let's begin by looking at",
        "Now, let's move on to",
        "Next, I'd like to discuss",
        "Let's explore",
        "Moving forward, let's examine",
        "Now let's turn our attention to",
        "Building on that, let's look at",
    ],
    Language.CHINESE: [
        "\u8ba9\u6211\u4eec\u9996\u5148\u770b\u770b",
        "\u63a5\u4e0b\u6765\uff0c\u8ba9\u6211\u4eec\u8ba8\u8bba",
        "\u73b0\u5728\u8ba9\u6211\u4eec\u6765\u770b\u770b",
        "\u4e0b\u9762\u6211\u4eec\u6765\u63a2\u8ba8",
        "\u63a5\u4e0b\u6765\u8ba9\u6211\u4eec\u5173\u6ce8",
    ],
    Language.JAPANESE: [
        "\u307e\u305a\u3001\u898b\u3066\u307f\u307e\u3057\u3087\u3046",
        "\u6b21\u306b\u3001\u8a71\u3057\u5408\u3044\u307e\u3057\u3087\u3046",
        "\u7d9a\u3044\u3066\u3001\u63a2\u3063\u3066\u307f\u307e\u3057\u3087\u3046",
        "\u3053\u3053\u3067\u306f\u3001\u78ba\u8a8d\u3057\u307e\u3057\u3087\u3046",
        "\u305d\u308c\u3067\u306f\u3001\u898b\u3066\u3044\u304d\u307e\u3057\u3087\u3046",
    ],
    Language.KOREAN: [
        "\uba3c\uc800 \uc0b4\ud3b4\ubcf4\uaca0\uc2b5\ub2c8\ub2e4",
        "\ub2e4\uc74c\uc73c\ub85c \ub118\uc5b4\uac00\uaca0\uc2b5\ub2c8\ub2e4",
        "\uc774\uc81c \ub2e4\uc74c \uc8fc\uc81c\ub97c \ub2e4\ub8e8\uaca0\uc2b5\ub2c8\ub2e4",
        "\uacc4\uc18d\ud574\uc11c \uc0b4\ud3b4\ubcf4\uaca0\uc2b5\ub2c8\ub2e4",
        "\uc774\uc5b4\uc11c \uc54c\uc544\ubcf4\uaca0\uc2b5\ub2c8\ub2e4",
    ],
    Language.FRENCH: [
        "Commen\u00e7ons par examiner",
        "Passons maintenant \u00e0",
        "Ensuite, parlons de",
        "Explorons maintenant",
        "Poursuivons avec",
    ],
    Language.GERMAN: [
        "Beginnen wir mit",
        "Kommen wir nun zu",
        "Als N\u00e4chstes betrachten wir",
        "Schauen wir uns an",
        "Fahren wir fort mit",
    ],
    Language.SPANISH: [
        "Comencemos por examinar",
        "Ahora, pasemos a",
        "A continuaci\u00f3n, hablemos de",
        "Exploremos ahora",
        "Sigamos adelante con",
    ],
}


def _build_speaker_notes(title: str, content: list, slide_idx: int,
                         total_content_slides: int, language: Language) -> str:
    """Build structured, conversational speaker notes for a slide."""
    phrases = _TRANSITION_PHRASES.get(language, _TRANSITION_PHRASES[Language.ENGLISH])
    transition = phrases[slide_idx % len(phrases)]

    # Build the main talking points from content
    points_text = " ".join(c[:80] for c in content[:3] if c and c != "Content placeholder")
    if not points_text:
        points_text = title

    if slide_idx == 0:
        # First content slide (title slide)
        notes = f"{transition} {title}. {points_text}."
    elif slide_idx >= total_content_slides - 1:
        # Last content slide
        if language == Language.CHINESE:
            notes = f"\u6700\u540e\uff0c\u8ba9\u6211\u4eec\u603b\u7ed3\u4e00\u4e0b\u3002{points_text}"
        elif language == Language.JAPANESE:
            notes = f"\u6700\u5f8c\u306b\u3001\u307e\u3068\u3081\u307e\u3057\u3087\u3046\u3002{points_text}"
        else:
            notes = f"Finally, let's wrap up with the key points. {points_text}"
    else:
        notes = f"{transition} {title}. {points_text}"

    return notes[:400]


def validate_content(slides: List[SlideData]) -> List[str]:
    """
    Validate slide content and return a list of warning messages.
    Checks for common issues like duplicate titles, empty content, and imbalanced slides.
    """
    warnings = []

    if not slides:
        warnings.append("No slides to validate.")
        return warnings

    # Check for duplicate titles
    titles = [s.title.strip().lower() for s in slides]
    seen = {}
    for i, t in enumerate(titles):
        if t in seen:
            warnings.append(f"Duplicate title: \"{slides[i].title}\" (slides {seen[t] + 1} and {i + 1})")
        else:
            seen[t] = i

    for i, slide in enumerate(slides):
        # Empty content on non-section/title slides
        if slide.layout in (SlideLayout.CONTENT, SlideLayout.TWO_COLUMN):
            if not slide.content or all(not c.strip() for c in slide.content):
                warnings.append(f"Slide {i + 1} \"{slide.title}\": no content bullet points")

        # Too many bullets
        if len(slide.content) > 8:
            warnings.append(
                f"Slide {i + 1} \"{slide.title}\": {len(slide.content)} bullets (recommended: 3-6)"
            )

        # Missing speaker notes
        if not slide.speaker_notes or not slide.speaker_notes.strip():
            warnings.append(f"Slide {i + 1} \"{slide.title}\": missing speaker notes")

        # Very long bullet points
        for j, point in enumerate(slide.content):
            if len(point) > 120:
                warnings.append(
                    f"Slide {i + 1}, bullet {j + 1}: too long ({len(point)} chars, max recommended: 120)"
                )

    return warnings


def mock_generate_content(text: str, num_slides: int, language: Language = Language.ENGLISH) -> List[SlideData]:
    """
    Generate slide content without an LLM by splitting text intelligently.
    Used as fallback or for testing without API keys.
    Produces a summary/key takeaways slide as the last slide.
    """
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n") if line.strip()]
    sentences = []
    for line in lines:
        for sep in ["\u3002", ".", "!", "\uff1f", "?", "\uff01", ";", "\uff1b", "\u2026"]:
            line = line.replace(sep, sep + "||SPLIT||")
        parts = [s.strip() for s in line.split("||SPLIT||") if s.strip()]
        sentences.extend(parts)

    if not sentences:
        sentences = ["Content placeholder"] * (num_slides * 3)

    # Reserve last slide for summary
    content_slides = max(1, num_slides - 1) if num_slides > 2 else num_slides
    slides = []
    chunk_size = max(1, len(sentences) // content_slides)

    for i in range(content_slides):
        start = i * chunk_size
        end = min(len(sentences), start + chunk_size)

        if start >= len(sentences):
            start = max(0, len(sentences) - chunk_size)
            end = len(sentences)

        chunk = sentences[start:end] if sentences[start:end] else ["Content placeholder"]

        title = chunk[0][:60] if len(chunk[0]) >= 5 else f"Slide {i + 1}"
        content = chunk[1:6] if len(chunk) > 1 else [chunk[0]]
        notes = _build_speaker_notes(title, content, i, content_slides, language)

        slides.append(SlideData(
            title=title,
            content=content,
            speaker_notes=notes,
            image_prompt=f"Professional presentation slide background, modern design, {title}",
        ))

    # Add summary/key takeaways slide
    if num_slides > 2:
        _SUMMARY_TITLES = {
            Language.ENGLISH: "Key Takeaways",
            Language.CHINESE: "\u6838\u5fc3\u8981\u70b9",
            Language.JAPANESE: "\u307e\u3068\u3081",
            Language.KOREAN: "\ud575\uc2ec \uc694\uc810",
            Language.FRENCH: "Points cl\u00e9s",
            Language.GERMAN: "Kernpunkte",
            Language.SPANISH: "Puntos clave",
        }
        summary_title = _SUMMARY_TITLES.get(language, "Key Takeaways")
        # Collect first sentence from each content slide as summary points
        summary_points = []
        for s in slides[1:]:  # skip title slide
            if s.content and s.content[0] != "Content placeholder":
                point = s.content[0][:80]
                summary_points.append(point)
        if not summary_points:
            summary_points = ["Review the key concepts discussed in this presentation"]
        slides.append(SlideData(
            title=summary_title,
            content=summary_points[:5],
            speaker_notes=f"In summary, these are the key points covered in this presentation.",
            image_prompt="Professional conclusion slide, abstract summary concept, clean modern design",
        ))

    slides = _assign_layouts(slides)

    # Insert TOC/agenda slide after title for presentations with 5+ slides
    if len(slides) >= 5:
        toc = _create_toc_slide(slides[1:], language)  # skip title slide
        slides.insert(1, toc)

    return slides


def llm_generate_content(
    text: str,
    api_key: str,
    base_url: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    num_slides: int = 5,
    language: Language = Language.ENGLISH,
    max_retries: int = 3,
    custom_prompt: str = "",
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

    prompt = _build_prompt(text, num_slides, language, custom_prompt=custom_prompt)
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
    custom_prompt: str = "",
) -> List[SlideData]:
    """
    Main entry point for content generation.
    Uses LLM if API key is provided, otherwise falls back to mock mode.
    """
    if api_key:
        return llm_generate_content(
            text, api_key, base_url, model, num_slides, language,
            custom_prompt=custom_prompt,
        )
    else:
        logger.info("No API key provided, using mock content generation")
        return mock_generate_content(text, num_slides, language)
