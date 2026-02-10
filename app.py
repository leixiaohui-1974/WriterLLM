"""
AutoPresentation AI - Main Streamlit Application
Transforms documents into professional presentations, PDFs, and videos.
Features: multi-language, themes, layouts, AI image generation, slide editor,
fade transitions, CJK support, and partial recovery.
"""
import os
import shutil
import logging

import streamlit as st

from src.config import setup_logging, DEFAULT_API_KEY, DEFAULT_BASE_URL, DEFAULT_MODEL
from src.models import (
    Language, SlideTheme, SlideData, SlideLayout, PresentationConfig, ExportFormat,
    MAX_UPLOAD_SIZE_MB, MAX_UPLOAD_SIZE_BYTES,
)
from src.parser import parse_document, SUPPORTED_EXTENSIONS
from src.generator import generate_slides, validate_content
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

# -- Session State Initialization --
_SESSION_DEFAULTS = {
    "slides_data": None,
    "extracted_text": None,
    "ai_bg_images": {},
    "phase": "upload",  # upload -> edit -> render
    "render_complete": False,
    "pptx_path": None,
    "pdf_path": None,
    "video_path": None,
    "image_paths": [],
    "srt_path": None,
}
for key, default in _SESSION_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default

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
    "forest": "Forest (Green)",
    "royal": "Royal (Purple)",
    "tech": "Tech (Cyan)",
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
speaking_rate_pct = st.sidebar.slider(
    "Speaking Rate",
    min_value=-50, max_value=50, value=0, step=10,
    help="Adjust TTS speaking speed (-50% slower to +50% faster).",
)
speaking_rate = f"+{speaking_rate_pct}%" if speaking_rate_pct >= 0 else f"{speaking_rate_pct}%"

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

# Footer branding
st.sidebar.divider()
st.sidebar.subheader("Footer Branding")
footer_company = st.sidebar.text_input(
    "Company Name",
    value="",
    help="Company or branding text shown at bottom-left of slides.",
)
footer_author = st.sidebar.text_input(
    "Author",
    value="",
    help="Author name shown at bottom-center of slides.",
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
    overlay_opacity = st.slider(
        "Background Overlay Opacity",
        min_value=0, max_value=255, value=130,
        help="Controls how much the theme overlay covers AI background images (0=transparent, 255=opaque).",
    )
    enable_animations = st.checkbox(
        "Bullet Animations (PPTX)",
        value=True,
        help="Enable click-to-appear entrance animations for bullet points in PowerPoint.",
    )
    transition_duration_ms = st.slider(
        "Transition Duration (ms)",
        min_value=200, max_value=2000, value=700, step=100,
        help="Duration of fade transitions between slides in PPTX.",
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
        overlay_opacity=overlay_opacity,
        speaking_rate=speaking_rate,
        footer_company=footer_company,
        footer_author=footer_author,
        enable_animations=enable_animations,
        transition_duration_ms=transition_duration_ms,
        export_formats=export_formats,
    )

    # File info
    st.info(f"File: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

    # ======================================================================
    # PHASE 1: Generate Content
    # ======================================================================
    if st.session_state.phase == "upload":
        if st.button("Generate Content", type="primary"):
            with st.spinner("Generating slide content..."):
                progress_bar = st.progress(0, text="Starting...")

                # Parse document
                progress_bar.progress(10, text="Parsing document...")
                text = parse_document(uploaded_file)
                st.session_state.extracted_text = text

                # Generate slides
                progress_bar.progress(30, text="Generating slide content...")
                mode = "AI" if config.api_key else "Mock"
                slides_data = generate_slides(
                    text,
                    num_slides=config.num_slides,
                    api_key=config.api_key,
                    base_url=config.base_url,
                    model=config.model,
                    language=config.language,
                    custom_prompt=config.custom_prompt,
                )
                st.session_state.slides_data = slides_data

                # Generate AI background images (if enabled)
                if enable_ai_images and config.api_key:
                    progress_bar.progress(50, text="Generating AI images...")
                    output_dir = "output"
                    bg_dir = os.path.join(output_dir, "backgrounds")
                    prompts = [(i, s.image_prompt) for i, s in enumerate(slides_data) if s.image_prompt]

                    def img_progress(current, total):
                        pct = 50 + int((current / max(total, 1)) * 40)
                        progress_bar.progress(min(pct, 90), text=f"Generating image {current + 1}/{total}...")

                    ai_bg_images = generate_slide_images_batch(
                        prompts, bg_dir,
                        api_key=config.api_key, base_url=config.base_url,
                        model=image_model, progress_callback=img_progress,
                    )
                    st.session_state.ai_bg_images = ai_bg_images
                    if ai_bg_images:
                        st.success(f"Generated {len(ai_bg_images)} AI background images.")

                progress_bar.progress(100, text="Content ready!")
                st.session_state.phase = "edit"
                st.rerun()

    # ======================================================================
    # PHASE 2: Slide Editor
    # ======================================================================
    if st.session_state.phase in ("edit", "render") and st.session_state.slides_data:
        slides = st.session_state.slides_data

        # Extracted text preview
        if st.session_state.extracted_text:
            with st.expander("Extracted Text Preview", expanded=False):
                text = st.session_state.extracted_text
                preview_len = min(len(text), 2000)
                st.text(text[:preview_len])
                if len(text) > preview_len:
                    st.caption(f"... ({len(text) - preview_len} more characters)")

        # Content validation warnings
        content_warnings = validate_content(slides)
        if content_warnings:
            with st.expander(f"Content Warnings ({len(content_warnings)})", expanded=False):
                for w in content_warnings:
                    st.warning(w)

        st.subheader("Slide Editor")
        st.caption("Edit slide content below, then click 'Create Presentation' to render.")

        # Layout label mapping
        layout_options = {
            SlideLayout.TITLE: "Title",
            SlideLayout.CONTENT: "Content",
            SlideLayout.SECTION: "Section",
            SlideLayout.TWO_COLUMN: "Two-Column",
        }
        layout_list = list(layout_options.keys())
        layout_labels = list(layout_options.values())

        # Track slides to delete
        slides_to_delete = []

        for i, slide in enumerate(slides):
            layout_badge = f"`{slide.layout.value}`"
            with st.expander(f"Slide {i + 1}: {slide.title} {layout_badge}", expanded=(i == 0)):
                col1, col2 = st.columns([3, 1])

                with col1:
                    new_title = st.text_input(
                        "Title", value=slide.title, key=f"title_{i}",
                    )
                    slides[i].title = new_title

                with col2:
                    current_idx = layout_list.index(slide.layout) if slide.layout in layout_list else 1
                    new_layout = st.selectbox(
                        "Layout", options=layout_list,
                        format_func=lambda x: layout_options[x],
                        index=current_idx, key=f"layout_{i}",
                    )
                    slides[i].layout = new_layout

                # Content bullets
                content_text = "\n".join(slide.content) if slide.content else ""
                new_content = st.text_area(
                    "Content (one bullet point per line)",
                    value=content_text, height=120, key=f"content_{i}",
                )
                slides[i].content = [line.strip() for line in new_content.split("\n") if line.strip()]

                # Speaker notes
                new_notes = st.text_area(
                    "Speaker Notes",
                    value=slide.speaker_notes, height=80, key=f"notes_{i}",
                )
                slides[i].speaker_notes = new_notes

                # Image prompt
                new_img_prompt = st.text_input(
                    "Image Prompt (for AI background)",
                    value=slide.image_prompt, key=f"img_prompt_{i}",
                )
                slides[i].image_prompt = new_img_prompt

                # Actions row
                action_cols = st.columns(4)
                with action_cols[0]:
                    if i > 0 and st.button("\u2191 Move Up", key=f"up_{i}"):
                        slides[i - 1], slides[i] = slides[i], slides[i - 1]
                        st.session_state.slides_data = slides
                        st.rerun()
                with action_cols[1]:
                    if i < len(slides) - 1 and st.button("\u2193 Move Down", key=f"down_{i}"):
                        slides[i], slides[i + 1] = slides[i + 1], slides[i]
                        st.session_state.slides_data = slides
                        st.rerun()
                with action_cols[2]:
                    if len(slides) > 1 and st.button("\u2717 Delete", key=f"del_{i}"):
                        slides_to_delete.append(i)

        # Process deletions
        if slides_to_delete:
            for idx in sorted(slides_to_delete, reverse=True):
                slides.pop(idx)
            st.session_state.slides_data = slides
            st.rerun()

        # Add new slide button
        if st.button("+ Add Slide"):
            new_slide = SlideData(
                title=f"Slide {len(slides) + 1}",
                content=["New content point"],
                speaker_notes="Speaker notes here.",
                image_prompt="Professional presentation visual",
                layout=SlideLayout.CONTENT,
            )
            slides.append(new_slide)
            st.session_state.slides_data = slides
            st.rerun()

        st.divider()

        # Action buttons
        btn_cols = st.columns(3)
        with btn_cols[0]:
            create_btn = st.button("Create Presentation", type="primary")
        with btn_cols[1]:
            if st.button("Regenerate Content"):
                st.session_state.phase = "upload"
                st.session_state.slides_data = None
                st.session_state.ai_bg_images = {}
                st.session_state.render_complete = False
                st.rerun()

        # ======================================================================
        # PHASE 3: Render Presentation
        # ======================================================================
        if create_btn:
            output_dir = "output"
            progress_bar = st.progress(0, text="Starting render...")
            status = st.empty()

            pptx_path = None
            pdf_path = None
            video_path = None
            image_paths = []
            ai_bg_images = st.session_state.ai_bg_images

            try:
                # Ensure output directory exists (no destructive cleanup)
                os.makedirs(output_dir, exist_ok=True)

                # Render PPTX
                if ExportFormat.PPTX in config.export_formats:
                    progress_bar.progress(10, text="Creating PowerPoint...")
                    status.markdown("**Step 1/4:** Creating PowerPoint file...")

                    pptx_path = os.path.join(output_dir, "presentation.pptx")
                    create_pptx_file(
                        slides, pptx_path, theme=config.theme,
                        background_images=ai_bg_images if ai_bg_images else None,
                        footer_company=config.footer_company,
                        footer_author=config.footer_author,
                        enable_animations=config.enable_animations,
                        transition_duration_ms=config.transition_duration_ms,
                    )

                # Slide Images (needed for PDF and video)
                progress_bar.progress(30, text="Rendering slide images...")
                status.markdown("**Step 2/4:** Rendering slide images...")
                images_dir = os.path.join(output_dir, "images")
                image_paths = create_slide_images(
                    slides, images_dir, theme=config.theme,
                    background_images=ai_bg_images if ai_bg_images else None,
                    language=config.language,
                    overlay_opacity=config.overlay_opacity,
                    footer_company=config.footer_company,
                    footer_author=config.footer_author,
                )

                # PDF
                if ExportFormat.PDF in config.export_formats:
                    progress_bar.progress(50, text="Generating PDF...")
                    status.markdown("**Step 3/4:** Generating PDF...")
                    pdf_path = os.path.join(output_dir, "presentation.pdf")
                    create_pdf_from_images(image_paths, pdf_path)

                # Video
                if ExportFormat.VIDEO in config.export_formats:
                    progress_bar.progress(60, text="Creating video with voiceover...")
                    status.markdown("**Step 4/4:** Generating video with AI voiceover...")

                    video_path = os.path.join(output_dir, "presentation.mp4")
                    voice = config.voice_name
                    scripts = [s.speaker_notes for s in slides]

                    def video_progress(current, total):
                        pct = 60 + int((current / max(total, 1)) * 35)
                        progress_bar.progress(min(pct, 95), text=f"Processing slide {current + 1}/{total}...")

                    try:
                        create_video_presentation(
                            image_paths, scripts, video_path,
                            voice=voice, progress_callback=video_progress,
                            speaking_rate=config.speaking_rate,
                        )
                    except Exception as e:
                        logger.error("Video generation failed: %s", e)
                        video_path = None
                        st.warning(f"Video generation failed: {e}. Other outputs are still available.")

                progress_bar.progress(100, text="Done!")
                status.markdown("**All steps completed!**")

                # Store results
                st.session_state.pptx_path = pptx_path
                st.session_state.pdf_path = pdf_path
                st.session_state.video_path = video_path
                st.session_state.image_paths = image_paths
                # SRT subtitle file is auto-generated alongside video
                srt_path = os.path.join(output_dir, "presentation.srt")
                st.session_state.srt_path = srt_path if os.path.exists(srt_path) else None
                st.session_state.render_complete = True
                st.session_state.phase = "render"

            except Exception as e:
                logger.error("Pipeline error: %s", e, exc_info=True)
                progress_bar.empty()
                status.empty()
                st.error(f"Error: {e}")

        # ======================================================================
        # Show Results
        # ======================================================================
        if st.session_state.render_complete:
            pptx_path = st.session_state.pptx_path
            pdf_path = st.session_state.pdf_path
            video_path = st.session_state.video_path
            image_paths = st.session_state.image_paths
            ai_bg_images = st.session_state.ai_bg_images

            has_any_output = pptx_path or pdf_path or video_path or image_paths
            if has_any_output:
                st.divider()
                st.header("Results")

                # Slide preview - show all slides in rows of 3
                if image_paths:
                    st.subheader("Slide Preview")
                    for row_start in range(0, len(image_paths), 3):
                        row_end = min(row_start + 3, len(image_paths))
                        cols = st.columns(3)
                        for idx in range(row_start, row_end):
                            with cols[idx - row_start]:
                                st.image(image_paths[idx], caption=f"Slide {idx + 1}", use_container_width=True)
                                # Show speaker notes below each slide thumbnail
                                if idx < len(slides) and slides[idx].speaker_notes:
                                    st.caption(slides[idx].speaker_notes[:150])

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

                # SRT subtitle download
                srt_path = st.session_state.srt_path
                if srt_path and os.path.exists(srt_path):
                    with open(srt_path, "r", encoding="utf-8") as f:
                        st.download_button(
                            "Download Subtitles (SRT)",
                            f.read(),
                            file_name="presentation.srt",
                            mime="text/plain",
                        )

                # Video player
                if video_path and os.path.exists(video_path):
                    st.subheader("Video Preview")
                    st.video(video_path)

# -- Footer --
st.sidebar.divider()
st.sidebar.caption("AutoPresentation AI v9.0")
if not api_key:
    st.sidebar.info("Running in Mock Mode. Add an API key for AI-powered content and images.")
