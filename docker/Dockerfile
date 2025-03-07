FROM fedora:41

# Install system dependencies including Python packages
RUN dnf5 update -y && \
    dnf5 install -y \
    python3 \
    python3-devel \
    python3-pip \
    python3-numpy \
    python3-scipy \
    python3-cffi \
    python3-wheel \
    python3-setuptools \
    gcc \
    gcc-c++ \
    make \
    pkg-config \
    portaudio \
    portaudio-devel \
    alsa-lib \
    alsa-lib-devel \
    ffmpeg \
    curl \
    git \
    redhat-rpm-config \
    libffi-devel \
    && dnf5 clean all

WORKDIR /usr/src/app

# Configure environment
ENV PIP_CERT=/etc/ssl/certs/ca-certificates.crt
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV PYTHONUNBUFFERED=1

# Install audio packages first
RUN PORTAUDIO_PATH=/usr/lib64/pkgconfig python3 -m pip install --no-cache-dir PyAudio && \
    python3 -m pip install --no-cache-dir sounddevice

# Install other Python packages
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy application files and setup environment
COPY src/ ./src/
RUN mkdir -p /usr/src/app/src/audio && \
    echo '{"user_input": [], "llm_response": []}' > /usr/src/app/src/memory.json && \
    chmod -R 777 /usr/src/app/src

EXPOSE 3000

CMD ["python3", "src/main.py"]
