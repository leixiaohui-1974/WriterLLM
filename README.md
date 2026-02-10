# AutoPresentation AI

A web application that transforms documents (Word, PDF, TXT, Markdown) into professional presentations (PPTX), PDFs, and videos with AI-generated content, images, and voiceovers.

## Features

### Document Processing
- **Multi-Format Parsing**: Extracts text from `.docx`, `.pdf`, `.txt`, and `.md` files with heading structure preservation
- **Smart Text Analysis**: Preserves document structure (headings, paragraphs) for better slide generation

### AI-Powered Content
- **LLM Content Generation**: Uses OpenAI-compatible LLMs with retry logic and response validation
- **Custom Prompts**: Provide additional instructions to guide AI content generation
- **AI Image Generation**: Generate background images for each slide using DALL-E or compatible APIs
- **Mock Mode**: Full pipeline works without API keys for testing and demos

### Multi-Language (7 Languages)
- English, Chinese, Japanese, Korean, French, German, Spanish
- Language-specific LLM prompts, TTS voices (male/female), and system prompts

### Presentation Design
- **5 Visual Themes**: Professional, Dark, Ocean, Sunset, Minimal
- **4 Slide Layouts**: Title, Content, Section Divider, Two-Column
- **Smart Layout Assignment**: Automatic layout selection based on content
- **Themed PPTX Output**: PowerPoint files match selected visual theme

### Output Formats
- **PowerPoint (PPTX)**: Editable files with themed colors, layouts, and speaker notes
- **PDF Export**: High-quality slide images compiled into PDF
- **Video (MP4)**: AI voiceovers with Microsoft Azure Neural TTS (edge-tts)
- **Selective Export**: Choose which formats to generate
- **Partial Recovery**: PPTX/PDF delivered even if video generation fails

### User Experience
- Real-time progress tracking with step-by-step status
- Slide preview grid with layout badges
- File size validation (50 MB limit)
- Advanced options panel with custom prompts and image model selection

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**:
   ```bash
   streamlit run app.py
   ```

3. **(Optional) Environment Variables**:
   ```bash
   export OPENAI_API_KEY="sk-..."
   export OPENAI_BASE_URL="https://api.openai.com/v1"
   export OPENAI_MODEL="gpt-4"
   ```

## Architecture

```
src/
├── __init__.py        # Package initialization
├── config.py          # Configuration management, env vars, constants
├── models.py          # Data models (SlideData, themes, languages, layouts, voices)
├── parser.py          # Document text extraction (DOCX, PDF, TXT, MD)
├── generator.py       # AI content generation with LLM + layout assignment
├── renderer.py        # Themed PPTX, layout-aware image rendering, PDF export
├── video.py           # TTS voiceover generation and video assembly
└── image_gen.py       # AI image generation for slide backgrounds
app.py                 # Main Streamlit application
```

## Testing

```bash
pytest -v
```

## Supported Languages

| Language | Content | TTS Voice (M/F) | Prompt |
|----------|---------|------------------|--------|
| English  | Yes     | Yes              | Full   |
| Chinese  | Yes     | Yes              | Full   |
| Japanese | Yes     | Yes              | Full   |
| Korean   | Yes     | Yes              | Full   |
| French   | Yes     | Yes              | Full   |
| German   | Yes     | Yes              | Full   |
| Spanish  | Yes     | Yes              | Full   |

## Requirements

- Python 3.8+
- `ffmpeg` (installed automatically via `imageio-ffmpeg` or system package)
