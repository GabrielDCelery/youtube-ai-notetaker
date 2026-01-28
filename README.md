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

## How to run it

The project uses [mise](https://mise.jdx.dev/) to make installing dependencies and running tasks easier. Check the `mise.toml` file to see what dependencies are installed.

### 1. Install dependencies

```bash
mise install
```

### 2. Get Ollama server running

```bash
ollama serve
ollama pull llama3.1:8b  # for topic segmentation and summaries
ollama pull llava        # for visual analysis (full mode only)

# Check if the server is reachable
nc -zv localhost 11434
```

### 3. Package the project

```bash
uv venv
uv sync
uv pip install .
# or uv pip install -e . for development
source .venv/bin/activate

# Verify installation
which ytainotetaker
```

### 4. Run it

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
