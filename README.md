# AutoPresentation AI

A web application that transforms documents (Word, PDF, TXT, Markdown) into professional presentations (PPTX), PDFs, and videos with AI-generated content and voiceovers.

## Features

- **Multi-Format Document Parsing**: Extracts text from `.docx`, `.pdf`, `.txt`, and `.md` files with heading structure preservation
- **AI Content Generation**: Uses OpenAI-compatible LLMs to generate structured slide content with retry logic and validation
- **Multi-Language Support**: Generate content and voiceovers in 7 languages (English, Chinese, Japanese, Korean, French, German, Spanish)
- **5 Slide Themes**: Professional, Dark, Ocean, Sunset, and Minimal visual themes
- **PowerPoint Generation**: Creates editable `.pptx` files with titles, bullet points, and speaker notes
- **Slide Image Rendering**: High-quality 1920x1080 slide images with theme-aware layouts
- **PDF Export**: Compiles slide images into a PDF document
- **Video Creation**: AI-generated voiceovers with Microsoft Azure Neural TTS (via edge-tts)
- **Progress Tracking**: Real-time progress bar with step-by-step status updates
- **Mock Mode**: Full pipeline works without API keys for testing and demos

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

## Usage

1. Open the app in your browser (default: `http://localhost:8501`)
2. Select language and slide theme in the sidebar
3. Upload a document (DOCX, PDF, TXT, or Markdown)
4. (Optional) Configure API key for AI-powered content generation
5. Adjust settings (number of slides, voice gender)
6. Click **Generate Presentation**
7. Download PPTX, PDF, and Video outputs

## Architecture

```
src/
├── __init__.py        # Package initialization
├── config.py          # Configuration management, env vars, constants
├── models.py          # Data models (SlideData, themes, languages, voices)
├── parser.py          # Document text extraction (DOCX, PDF, TXT, MD)
├── generator.py       # AI content generation with LLM integration
├── renderer.py        # PPTX creation, slide image rendering, PDF export
└── video.py           # TTS voiceover generation and video assembly
app.py                 # Main Streamlit application
```

## Testing

```bash
pytest -v
```

## Supported Languages

| Language | Content Generation | TTS Voice (M/F) |
|----------|-------------------|------------------|
| English  | Yes               | Yes              |
| Chinese  | Yes               | Yes              |
| Japanese | Yes               | Yes              |
| Korean   | Yes               | Yes              |
| French   | Yes               | Yes              |
| German   | Yes               | Yes              |
| Spanish  | Yes               | Yes              |

## Requirements

- Python 3.8+
- `ffmpeg` (installed automatically via `imageio-ffmpeg` or system package)
