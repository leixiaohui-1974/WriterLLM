"""
AutoPresentation AI - Main Streamlit Application
Transforms documents into professional presentations, PDFs, and videos.
Features: multi-language, themes, layouts, AI image generation, partial recovery.
"""
import os
import shutil
import logging

import streamlit as st

from src.config import setup_logging, DEFAULT_API_KEY, DEFAULT_BASE_URL, DEFAULT_MODEL
from src.models import (
    Language, SlideTheme, PresentationConfig, ExportFormat,
    MAX_UPLOAD_SIZE_MB, MAX_UPLOAD_SIZE_BYTES,
)
from src.parser import parse_document, SUPPORTED_EXTENSIONS
from src.generator import generate_slides
from src.renderer import create_pptx_file, create_slide_images, create_pdf_from_images
from src.video import create_video_presentation
from src.image_gen import generate_slide_images_batch

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

# Export options
st.sidebar.divider()
st.sidebar.subheader("Export Options")
export_pptx = st.sidebar.checkbox("PowerPoint (PPTX)", value=True)
export_pdf = st.sidebar.checkbox("PDF", value=True)
export_video = st.sidebar.checkbox("Video (MP4)", value=True)
enable_ai_images = st.sidebar.checkbox(
    "AI Slide Images",
    value=False,
    help="Generate AI background images for each slide (requires API key, adds generation time).",
)

# Advanced
with st.sidebar.expander("Advanced Options"):
    custom_prompt = st.text_area(
        "Custom Instructions",
        placeholder="e.g., 'Focus on technical details' or 'Use a formal tone'",
        help="Additional instructions for AI content generation.",
    )
    image_model = st.text_input(
        "Image Model",
        value="dall-e-3",
        help="Model for AI image generation (dall-e-3, dall-e-2, etc.).",
    )

# -- Main Content --
st.title("AutoPresentation AI")
st.markdown("Transform your documents into professional presentations, PDFs, and videos with AI.")

# File upload
file_types = list(SUPPORTED_EXTENSIONS)
uploaded_file = st.file_uploader(
    "Upload Document",
    type=file_types,
    help=f"Supported formats: {', '.join('.' + ext for ext in sorted(file_types))} (max {MAX_UPLOAD_SIZE_MB} MB)",
)

if uploaded_file:
    # File size validation
    if uploaded_file.size > MAX_UPLOAD_SIZE_BYTES:
        st.error(f"File too large ({uploaded_file.size / 1024 / 1024:.1f} MB). Maximum: {MAX_UPLOAD_SIZE_MB} MB.")
        st.stop()

    # Build export format list
    export_formats = []
    if export_pptx:
        export_formats.append(ExportFormat.PPTX)
    if export_pdf:
        export_formats.append(ExportFormat.PDF)
    if export_video:
        export_formats.append(ExportFormat.VIDEO)

    if not export_formats:
        st.warning("Please select at least one export format.")
        st.stop()

    # Build config
    config = PresentationConfig(
        num_slides=num_slides,
        language=language,
        voice_gender=voice_gender,
        theme=theme,
        api_key=api_key if api_key else None,
        base_url=base_url if base_url else None,
        model=model_name,
        custom_prompt=custom_prompt if custom_prompt else "",
        export_formats=export_formats,
    )

    # File info
    st.info(f"File: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

    if st.button("Generate Presentation", type="primary"):
        output_dir = "output"
        progress_bar = st.progress(0, text="Starting...")
        status = st.empty()

        # Track partial results for recovery
        pptx_path = None
        pdf_path = None
        video_path = None
        image_paths = []
        slides_data = []

        try:
            # -- Step 1: Parse Document --
            progress_bar.progress(5, text="Parsing document...")
            status.markdown("**Step 1/5:** Extracting text from document...")

            text = parse_document(uploaded_file)

            with st.expander("Extracted Text Preview", expanded=False):
                preview_len = min(len(text), 2000)
                st.text(text[:preview_len])
                if len(text) > preview_len:
                    st.caption(f"... ({len(text) - preview_len} more characters)")

            # -- Step 2: Generate Content --
            progress_bar.progress(15, text="Generating content...")
            mode = "AI" if config.api_key else "Mock"
            status.markdown(f"**Step 2/5:** Generating slide content ({mode} mode)...")

            slides_data = generate_slides(
                text,
                num_slides=config.num_slides,
                api_key=config.api_key,
                base_url=config.base_url,
                model=config.model,
                language=config.language,
                custom_prompt=config.custom_prompt,
            )

            with st.expander("Generated Slide Content", expanded=False):
                for i, slide in enumerate(slides_data):
                    layout_badge = f"`{slide.layout.value}`"
                    st.markdown(f"**Slide {i+1}: {slide.title}** {layout_badge}")
                    for point in slide.content:
                        st.markdown(f"- {point}")
                    if slide.speaker_notes:
                        st.caption(f"Notes: {slide.speaker_notes[:120]}...")
                    st.divider()

            # -- Step 3: AI Image Generation (optional) --
            ai_bg_images = {}
            if enable_ai_images and config.api_key:
                progress_bar.progress(25, text="Generating AI images...")
                status.markdown("**Step 3/5:** Generating AI background images...")

                bg_dir = os.path.join(output_dir, "backgrounds")
                prompts = [(i, s.image_prompt) for i, s in enumerate(slides_data) if s.image_prompt]

                def img_progress(current, total):
                    pct = 25 + int((current / max(total, 1)) * 15)
                    progress_bar.progress(min(pct, 40), text=f"Generating image {current + 1}/{total}...")

                ai_bg_images = generate_slide_images_batch(
                    prompts, bg_dir,
                    api_key=config.api_key, base_url=config.base_url,
                    model=image_model, progress_callback=img_progress,
                )
                if ai_bg_images:
                    st.success(f"Generated {len(ai_bg_images)} AI background images.")
            else:
                progress_bar.progress(40, text="Skipping AI images...")

            # -- Step 4: Render Slides --
            progress_bar.progress(40, text="Rendering slides...")
            status.markdown("**Step 4/5:** Rendering presentations...")

            if os.path.exists(output_dir):
                # Preserve backgrounds dir if it exists
                bg_dir_path = os.path.join(output_dir, "backgrounds")
                bg_exists = os.path.exists(bg_dir_path)
                if bg_exists:
                    import tempfile
                    tmp = tempfile.mkdtemp()
                    shutil.copytree(bg_dir_path, os.path.join(tmp, "backgrounds"))
                shutil.rmtree(output_dir)
                os.makedirs(output_dir)
                if bg_exists:
                    shutil.copytree(os.path.join(tmp, "backgrounds"), bg_dir_path)
                    shutil.rmtree(tmp)
            else:
                os.makedirs(output_dir)

            # PPTX
            if ExportFormat.PPTX in config.export_formats:
                pptx_path = os.path.join(output_dir, "presentation.pptx")
                create_pptx_file(slides_data, pptx_path, theme=config.theme)

            progress_bar.progress(50, text="Creating slide images...")

            # Slide Images (always needed for PDF and video)
            images_dir = os.path.join(output_dir, "images")
            image_paths = create_slide_images(slides_data, images_dir, theme=config.theme)

            # PDF
            if ExportFormat.PDF in config.export_formats:
                progress_bar.progress(55, text="Generating PDF...")
                pdf_path = os.path.join(output_dir, "presentation.pdf")
                create_pdf_from_images(image_paths, pdf_path)

            # -- Step 5: Generate Video --
            if ExportFormat.VIDEO in config.export_formats:
                progress_bar.progress(60, text="Creating video with voiceover...")
                status.markdown("**Step 5/5:** Generating video with AI voiceover...")

                video_path = os.path.join(output_dir, "presentation.mp4")
                voice = config.voice_name
                scripts = [s.speaker_notes for s in slides_data]

                def video_progress(current, total):
                    pct = 60 + int((current / max(total, 1)) * 35)
                    progress_bar.progress(min(pct, 95), text=f"Processing slide {current + 1}/{total}...")

                try:
                    create_video_presentation(
                        image_paths, scripts, video_path,
                        voice=voice, progress_callback=video_progress,
                    )
                except Exception as e:
                    logger.error("Video generation failed: %s", e)
                    video_path = None
                    st.warning(f"Video generation failed: {e}. Other outputs are still available.")

            progress_bar.progress(100, text="Done!")
            status.markdown("**All steps completed!**")

        except Exception as e:
            logger.error("Pipeline error: %s", e, exc_info=True)
            progress_bar.empty()
            status.empty()
            st.error(f"Error: {e}")

        # -- Results (shown even if video failed) --
        has_any_output = pptx_path or pdf_path or video_path or image_paths
        if has_any_output:
            st.divider()
            st.header("Results")

            # Slide preview
            if image_paths:
                st.subheader("Slide Preview")
                preview_count = min(len(image_paths), 5)
                cols = st.columns(preview_count)
                for idx in range(preview_count):
                    with cols[idx]:
                        st.image(image_paths[idx], caption=f"Slide {idx + 1}", use_container_width=True)
                if len(image_paths) > preview_count:
                    st.caption(f"... and {len(image_paths) - preview_count} more slides")

            # AI-generated background previews
            if ai_bg_images:
                with st.expander("AI Generated Backgrounds", expanded=False):
                    bg_cols = st.columns(min(len(ai_bg_images), 4))
                    for idx, (slide_idx, bg_path) in enumerate(sorted(ai_bg_images.items())[:4]):
                        with bg_cols[idx]:
                            st.image(bg_path, caption=f"Slide {slide_idx + 1} BG", use_container_width=True)

            # Downloads
            st.subheader("Downloads")
            dl_cols = st.columns(3)

            with dl_cols[0]:
                if pptx_path and os.path.exists(pptx_path):
                    with open(pptx_path, "rb") as f:
                        st.download_button(
                            "Download PPTX",
                            f,
                            file_name="presentation.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True,
                        )

            with dl_cols[1]:
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "Download PDF",
                            f,
                            file_name="presentation.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )

            with dl_cols[2]:
                if video_path and os.path.exists(video_path):
                    with open(video_path, "rb") as f:
                        st.download_button(
                            "Download Video",
                            f,
                            file_name="presentation.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                        )

            # Video player
            if video_path and os.path.exists(video_path):
                st.subheader("Video Preview")
                st.video(video_path)

# -- Footer --
st.sidebar.divider()
st.sidebar.caption("AutoPresentation AI v2.1")
if not api_key:
    st.sidebar.info("Running in Mock Mode. Add an API key for AI-powered content and images.")
