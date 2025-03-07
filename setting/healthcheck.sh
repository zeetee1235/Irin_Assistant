#!/bin/bash

# Try to get a response from Ollama server
response=$(curl -s http://localhost:11434/api/tags)

# Check if the response is valid JSON
if echo "$response" | jq . >/dev/null 2>&1; then
    # Server is responding with valid JSON
    exit 0
else
    # Server is not responding properly
    exit 1
fi
