import os

import ollama

ollama_host = os.getenv("OLLAMA_HOST", "localhost")

# Configure Ollama client to use remote host
ollama_client = ollama.Client(host=f"{ollama_host}:11434")
