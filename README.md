# YouTube AI Notetaker

There are just so many technical videos on youtube that it takes too much time to watch them. This is a project to analyse those videos and create a `markdown` extract that I can scan through to figure out if it is worth my time.

![screenshot-youtube-ai-notetaker-001](./assets/screenshot-youtube-ai-notetaker-001.jpg)

![screenshot-youtube-ai-notetaker-002](./assets/screenshot-youtube-ai-notetaker-002.jpg)

## What it does

- Fetches YouTube transcript
- Uses LLM to segment video into topics
- Generates a markdown summary

**Full mode** additionally:
- Downloads the video
- Extracts frames from each segment
- Uses visual analysis (llava) to capture diagrams and code

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
