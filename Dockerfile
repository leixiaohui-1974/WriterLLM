FROM python:3.11-slim

# Install system dependencies: ffmpeg for video, CJK fonts for multilingual support
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    fonts-wqy-zenhei \
    fonts-ipafont-gothic \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /app/output

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
