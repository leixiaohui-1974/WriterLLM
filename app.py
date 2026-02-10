import streamlit as st
import os
import shutil
from src.parser import parse_document
from src.generator import generate_slides
from src.renderer import create_pptx_file, create_slide_images, create_pdf_from_images
from src.video import create_video_presentation

st.set_page_config(page_title="AutoPresentation AI", layout="wide")

st.title("AutoPresentation AI")
st.markdown("Generates PPT, PDF, and Video from your documents using AI.")

# Sidebar Settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("OpenAI API Key (Optional)", type="password", help="Leave empty to use Mock Mode.")
base_url = st.sidebar.text_input("API Base URL (Optional)", help="e.g. https://api.doubao.com/v1")
model_name = st.sidebar.text_input("Model Name (Optional)", value="gpt-3.5-turbo", help="e.g. gpt-4, doubao-pro-4k")
num_slides = st.sidebar.slider("Number of Slides", 3, 20, 5)
voice_gender = st.sidebar.selectbox("Voice Gender", ["Male", "Female"])

uploaded_file = st.file_uploader("Upload Document (Word or PDF)", type=['docx', 'pdf'])

if uploaded_file:
    if st.button("Generate Presentation"):
        with st.spinner("Processing Document..."):
            # 1. Parse
            try:
                text = parse_document(uploaded_file)
                st.success("Document parsed successfully.")
                with st.expander("View Extracted Text"):
                    st.text(text[:1000] + "...")
            except Exception as e:
                st.error(f"Error parsing document: {e}")
                st.stop()

        with st.spinner("Generating Content (AI)..."):
            # 2. Generate Content
            try:
                slides_data = generate_slides(
                    text,
                    num_slides=num_slides,
                    api_key=api_key if api_key else None,
                    base_url=base_url if base_url else None,
                    model=model_name
                )
                st.success("Content generated.")
                with st.expander("View Slide Content"):
                    st.json(slides_data)
            except Exception as e:
                st.error(f"Error generating content: {e}")
                st.stop()

        with st.spinner("Rendering Slides..."):
            # 3. Render
            try:
                output_dir = "output"
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
                os.makedirs(output_dir)

                # PPTX
                pptx_path = os.path.join(output_dir, "presentation.pptx")
                create_pptx_file(slides_data, pptx_path)

                # Images
                images_dir = os.path.join(output_dir, "images")
                image_paths = create_slide_images(slides_data, images_dir)

                # PDF
                pdf_path = os.path.join(output_dir, "presentation.pdf")
                create_pdf_from_images(image_paths, pdf_path)

                st.success("Slides rendered.")
            except Exception as e:
                st.error(f"Error rendering slides: {e}")
                st.stop()

        with st.spinner("Creating Video..."):
            # 4. Video
            try:
                video_path = os.path.join(output_dir, "presentation.mp4")
                # Voice selection
                voice = "en-US-ChristopherNeural" if voice_gender == "Male" else "en-US-JennyNeural"

                scripts = [s.get("speaker_notes", "") for s in slides_data]
                create_video_presentation(image_paths, scripts, video_path, voice=voice)
                st.success("Video created.")
            except Exception as e:
                st.error(f"Error creating video: {e}")
                st.stop()

        # Display Results
        st.divider()
        st.header("Results")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Presentation")
            # Show first image
            if image_paths:
                st.image(image_paths[0], caption="Title Slide")

            with open(pptx_path, "rb") as f:
                st.download_button("Download PPTX", f, file_name="presentation.pptx")

            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF", f, file_name="presentation.pdf")

        with col2:
            st.subheader("Video")
            if os.path.exists(video_path):
                st.video(video_path)
                with open(video_path, "rb") as f:
                    st.download_button("Download Video", f, file_name="presentation.mp4")
