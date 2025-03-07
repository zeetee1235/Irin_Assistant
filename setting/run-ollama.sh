#!/bin/sh

# Start Ollama server in the background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
echo "Waiting for Ollama server to start..."
sleep 10

# Create irin model
echo "Creating Irin model..."
if [ -f /model/Modelfile ]; then
    ollama create irin -f /model/Modelfile
    echo "Irin model created successfully"
else
    echo "Modelfile not found in /model directory"
    exit 1
fi

# Wait for the background process
wait $OLLAMA_PID
