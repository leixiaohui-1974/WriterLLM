import json
import os
from typing import List, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def mock_generate_content(text: str, num_slides: int) -> List[Dict[str, Any]]:
    """
    Generates dummy slide content based on input text without using an LLM.
    Splits text into chunks to simulate slides.
    """
    # Simple heuristic: split by sentences
    sentences = [s.strip() for s in text.replace('\n', '.').split('.') if s.strip()]
    if not sentences:
        sentences = ["Default Content"] * (num_slides * 5)

    slides = []
    chunk_size = max(1, len(sentences) // num_slides)

    for i in range(num_slides):
        start = i * chunk_size
        end = min(len(sentences), start + chunk_size)

        # Ensure we have content
        if start >= len(sentences):
            start = 0
            end = chunk_size

        slide_sentences = sentences[start:end]

        # Fallback if text is still somehow empty
        if not slide_sentences:
            slide_sentences = ["Content placeholder..."]

        title = slide_sentences[0][:50]
        if len(title) < 5: title = f"Slide {i+1}"

        content = slide_sentences[1:5] if len(slide_sentences) > 1 else ["Point 1", "Point 2"]
        notes = " ".join(slide_sentences)

        slide = {
            "title": title,
            "content": content,
            "speaker_notes": notes[:200] + "...", # Truncate for demo
            "image_prompt": f"A professional presentation background about {title}"
        }
        slides.append(slide)

    return slides

def llm_generate_content(text: str, api_key: str, base_url: str = None, model: str = "gpt-3.5-turbo", num_slides: int = 5) -> List[Dict[str, Any]]:
    """
    Uses an LLM to generate structured JSON for slides.
    """
    if not OpenAI:
        raise ImportError("OpenAI library not installed.")

    # Allow user to override base_url for non-OpenAI endpoints (e.g. Doubao via proxy)
    client = OpenAI(api_key=api_key, base_url=base_url)

    prompt = f"""
    You are a professional presentation assistant.
    Analyze the following text and create a {num_slides}-slide presentation.
    Return a JSON object with a key "slides" containing an array of slide objects.
    Each slide object must have:
    - "title": string
    - "content": list of strings (bullet points)
    - "speaker_notes": string (script for the presenter, natural language)
    - "image_prompt": string (description for an AI image generator)

    Text to analyze:
    {text[:4000]}
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        data = json.loads(content)

        if "slides" in data:
            return data["slides"]
        elif isinstance(data, list):
            return data
        else:
            # Try to find a list in the values
            for v in data.values():
                if isinstance(v, list):
                    return v
            return mock_generate_content(text, num_slides)

    except Exception as e:
        print(f"LLM Error: {e}. Falling back to mock.")
        return mock_generate_content(text, num_slides)

def generate_slides(text: str, num_slides: int = 5, api_key: str = None, base_url: str = None, model: str = "gpt-3.5-turbo") -> List[Dict[str, Any]]:
    """
    Main entry point for content generation.
    """
    if api_key:
        return llm_generate_content(text, api_key, base_url, model, num_slides)
    else:
        return mock_generate_content(text, num_slides)
