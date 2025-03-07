#!/bin/bash

# Wait for Ollama server to be ready
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    echo "Waiting for Ollama server..."
    sleep 5
done

# Create Irin model
echo "Creating Irin model..."
ollama create irin -f /model/Modelfile

echo "Initialization complete"
