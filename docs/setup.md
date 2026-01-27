# Setup

## Requirements

- Ollama server running (`ollama serve`)
- Required models:
  - `ollama pull llama3.1:8b` - Topic segmentation and summaries
  - `ollama pull llava` - Visual/frame analysis (full mode only)

## Installation

```bash
mise install                 # Install Python, Ollama, uv
uv venv && uv sync           # Create venv and install deps
uv pip install .             # Install CLI entry point
```

## Usage

```bash
# Quick mode (default) - transcript only
ytainotetaker "https://www.youtube.com/watch?v=VIDEO_ID"

# Full mode - includes visual analysis
ytainotetaker --mode full "https://www.youtube.com/watch?v=VIDEO_ID"

# With custom directories
ytainotetaker --mode full -d ./downloads -o ./output "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Environment

- `OLLAMA_HOST` - Ollama server URL (optional, defaults to `http://localhost:11434`)
