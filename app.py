"""
AutoPresentation AI - Main Streamlit Application
Transforms documents into professional presentations, PDFs, and videos.
"""
import os
import shutil
import logging

import streamlit as st

from src.config import setup_logging, DEFAULT_API_KEY, DEFAULT_BASE_URL, DEFAULT_MODEL
from src.models import Language, SlideTheme, PresentationConfig
from src.parser import parse_document, SUPPORTED_EXTENSIONS
from src.generator import generate_slides
from src.renderer import create_pptx_file, create_slide_images, create_pdf_from_images
from src.video import create_video_presentation

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# -- Page Config --
st.set_page_config(
    page_title="AutoPresentation AI",
    page_icon="\U0001F3AC",
    layout="wide",
)

# -- Sidebar Settings --
st.sidebar.header("Settings")

# Language
language_options = {lang.value: lang for lang in Language}
language_labels = {
    "en": "English", "zh": "Chinese / \u4e2d\u6587", "ja": "Japanese / \u65e5\u672c\u8a9e",
    "ko": "Korean / \ud55c\uad6d\uc5b4", "fr": "French / Fran\u00e7ais",
    "de": "German / Deutsch", "es": "Spanish / Espa\u00f1ol",
}
selected_lang = st.sidebar.selectbox(
    "Language",
    options=list(language_labels.keys()),
    format_func=lambda x: language_labels[x],
    index=0,
)
language = language_options[selected_lang]

# Theme
theme_labels = {
    "professional": "Professional (Blue)",
    "dark": "Dark Mode",
    "ocean": "Ocean",
    "sunset": "Sunset",
    "minimal": "Minimal",
}
selected_theme = st.sidebar.selectbox(
    "Slide Theme",
    options=list(theme_labels.keys()),
    format_func=lambda x: theme_labels[x],
    index=0,
)
theme = SlideTheme(selected_theme)

# AI Settings
st.sidebar.divider()
st.sidebar.subheader("AI Configuration")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    value=DEFAULT_API_KEY,
    type="password",
    help="Leave empty to use Mock Mode (no API required).",
)
base_url = st.sidebar.text_input(
    "API Base URL",
    value=DEFAULT_BASE_URL,
    help="For OpenAI-compatible endpoints (e.g., Doubao, Ollama).",
)
model_name = st.sidebar.text_input(
    "Model Name",
    value=DEFAULT_MODEL or "gpt-3.5-turbo",
)

# Presentation Settings
st.sidebar.divider()
st.sidebar.subheader("Presentation")
num_slides = st.sidebar.slider("Number of Slides", 3, 20, 5)
voice_gender = st.sidebar.selectbox("Voice Gender", ["Female", "Male"])

# -- Main Content --
st.title("AutoPresentation AI")
st.markdown("Transform your documents into professional presentations, PDFs, and videos with AI.")

# File upload
file_types = list(SUPPORTED_EXTENSIONS)
uploaded_file = st.file_uploader(
    "Upload Document",
    type=file_types,
    help=f"Supported formats: {', '.join('.' + ext for ext in sorted(file_types))}",
)

if uploaded_file:
    # Build config
    config = PresentationConfig(
        num_slides=num_slides,
        language=language,
        voice_gender=voice_gender,
        theme=theme,
        api_key=api_key if api_key else None,
        base_url=base_url if base_url else None,
        model=model_name,
    )

    # Show file info
    st.info(f"File: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

    if st.button("Generate Presentation", type="primary"):
        output_dir = "output"
        progress_bar = st.progress(0, text="Starting...")
        status = st.empty()

        try:
            # -- Step 1: Parse Document --
            progress_bar.progress(5, text="Parsing document...")
            status.markdown("**Step 1/4:** Extracting text from document...")

            text = parse_document(uploaded_file)

            with st.expander("Extracted Text Preview", expanded=False):
                preview_len = min(len(text), 2000)
                st.text(text[:preview_len])
                if len(text) > preview_len:
                    st.caption(f"... ({len(text) - preview_len} more characters)")

            # -- Step 2: Generate Content --
            progress_bar.progress(20, text="Generating content...")
            mode = "AI" if config.api_key else "Mock"
            status.markdown(f"**Step 2/4:** Generating slide content ({mode} mode)...")

            slides_data = generate_slides(
                text,
                num_slides=config.num_slides,
                api_key=config.api_key,
                base_url=config.base_url,
                model=config.model,
                language=config.language,
            )

            with st.expander("Generated Slide Content", expanded=False):
                for i, slide in enumerate(slides_data):
                    st.markdown(f"**Slide {i+1}: {slide.title}**")
                    for point in slide.content:
                        st.markdown(f"- {point}")
                    if slide.speaker_notes:
                        st.caption(f"Notes: {slide.speaker_notes[:100]}...")
                    st.divider()

            # -- Step 3: Render Slides --
            progress_bar.progress(40, text="Rendering slides...")
            status.markdown("**Step 3/4:** Rendering presentations...")

            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)

            # PPTX
            pptx_path = os.path.join(output_dir, "presentation.pptx")
            create_pptx_file(slides_data, pptx_path)

            progress_bar.progress(50, text="Creating slide images...")

            # Slide Images
            images_dir = os.path.join(output_dir, "images")
            image_paths = create_slide_images(slides_data, images_dir, theme=config.theme)

            progress_bar.progress(60, text="Generating PDF...")

            # PDF
            pdf_path = os.path.join(output_dir, "presentation.pdf")
            create_pdf_from_images(image_paths, pdf_path)

            # -- Step 4: Generate Video --
            progress_bar.progress(70, text="Creating video with voiceover...")
            status.markdown("**Step 4/4:** Generating video with AI voiceover...")

            video_path = os.path.join(output_dir, "presentation.mp4")
            voice = config.voice_name
            scripts = [s.speaker_notes for s in slides_data]

            def video_progress(current, total):
                pct = 70 + int((current / max(total, 1)) * 25)
                progress_bar.progress(min(pct, 95), text=f"Processing slide {current + 1}/{total}...")

            create_video_presentation(image_paths, scripts, video_path, voice=voice, progress_callback=video_progress)

            progress_bar.progress(100, text="Done!")
            status.markdown("**All steps completed successfully!**")

            # -- Results --
            st.divider()
            st.header("Results")

            # Slide preview
            if image_paths:
                st.subheader("Slide Preview")
                cols = st.columns(min(len(image_paths), 4))
                for idx, img_path in enumerate(image_paths[:4]):
                    with cols[idx]:
                        st.image(img_path, caption=f"Slide {idx + 1}", use_container_width=True)
                if len(image_paths) > 4:
                    st.caption(f"... and {len(image_paths) - 4} more slides")

            # Downloads
            st.subheader("Downloads")
            dl_col1, dl_col2, dl_col3 = st.columns(3)

            with dl_col1:
                with open(pptx_path, "rb") as f:
                    st.download_button(
                        "Download PPTX",
                        f,
                        file_name="presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True,
                    )

            with dl_col2:
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "Download PDF",
                            f,
                            file_name="presentation.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )

            with dl_col3:
                if os.path.exists(video_path):
                    with open(video_path, "rb") as f:
                        st.download_button(
                            "Download Video",
                            f,
                            file_name="presentation.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                        )

            # Video player
            if os.path.exists(video_path):
                st.subheader("Video Preview")
                st.video(video_path)

        except Exception as e:
            logger.error("Pipeline error: %s", e, exc_info=True)
            progress_bar.empty()
            status.empty()
            st.error(f"Error: {e}")

# -- Footer --
st.sidebar.divider()
st.sidebar.caption("AutoPresentation AI v2.0")
if not api_key:
    st.sidebar.info("Running in Mock Mode. Add an API key for AI-powered content.")
