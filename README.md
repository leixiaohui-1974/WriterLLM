# AutoPresentation AI

A powerful web application that transforms your documents (Word, PDF) into professional presentations (PPTX), PDFs, and Videos with AI-generated content and voiceovers.

## Features

- **Document Parsing**: Extracts text from `.docx` and `.pdf` files.
- **AI Content Generation**: Uses OpenAI/Doubao-compatible LLMs to generate structured slide content, including titles, bullet points, and speaker notes.
- **PowerPoint Generation**: Creates editable `.pptx` files.
- **Slide Rendering**: Generates high-quality slide images using Python (Pillow).
- **Video Creation**: Synthesizes a video presentation by combining slide images with AI-generated voiceovers (using `edge-tts`).
- **PDF Export**: Compiles slide images into a PDF document.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

3.  **Usage**:
    - Open the app in your browser (default: `http://localhost:8501`).
    - Upload a document.
    - (Optional) Enter your OpenAI API Key or compatible Base URL (e.g., for Doubao via an OpenAI-compatible proxy).
    - Adjust settings (Number of slides, Voice).
    - Click "Generate Presentation".
    - Download your PPTX, PDF, and Video!

## Architecture

- `src/parser.py`: Handles document text extraction.
- `src/generator.py`: Interfaces with LLMs to structure content. Includes a Mock Mode for testing without API keys.
- `src/renderer.py`: Generates `.pptx` files and renders slide images using Pillow.
- `src/video.py`: Handles Text-to-Speech generation and video assembly using MoviePy.
- `app.py`: Main Streamlit application.

## Requirements

- Python 3.8+
- `ffmpeg` (installed automatically via `imageio-ffmpeg` or system package)
