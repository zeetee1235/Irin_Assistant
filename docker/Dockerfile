FROM python:3.9-slim

LABEL maintainer="Irin Assistant"
LABEL version="1.0"

# Install system dependencies with all required audio libraries
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    portaudio19-dev \
    python3-pyaudio \
python3-all-dev \
    python3-numpy \
    ffmpeg \
curl \
pkg-config \
    build-essential \
    libasound2-dev \
libportaudio2 \
    libportaudiocpp0 \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Install Python packages in the correct order
COPY requirements.txt .
RUN pip install --upgrade pip && \
pip install --no-cache-dir wheel setuptools && \
pip install --no-cache-dir PyAudio && \
pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Create necessary directories and files
RUN mkdir -p /usr/src/app/src/audio && \
echo '{"user_input": [], "llm_response": []}' > /usr/src/app/src/memory.json && \
chmod -R 777 /usr/src/app/src

EXPOSE 3000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

CMD ["python", "src/main.py"]
