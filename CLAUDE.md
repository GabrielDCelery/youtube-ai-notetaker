# CLAUDE.md

This file provides guidance for Claude Code when working with this repository.

## Project Overview

YouTube AI Notetaker is a CLI tool that generates comprehensive markdown notes from YouTube videos. It downloads videos, extracts frames, fetches transcripts, and uses local LLMs via Ollama to create detailed technical documentation.

## Architecture

```
src/youtube_ai_notetaker/
├── cli.py                    # Entry point - ytainotetaker command
├── video/
│   ├── video_id.py          # YouTube URL parsing
│   ├── downloader.py        # Video download via yt-dlp
│   └── frames.py            # Frame extraction via OpenCV
├── transcript/
│   └── fetcher.py           # YouTube transcript API
├── analysis/
│   ├── ollama.py            # Ollama client configuration
│   ├── visual.py            # Frame analysis with llava model
│   └── summary.py           # Summary generation with llama3.2
├── utils/
│   └── formatter.py         # Timestamp formatting
└── instructions/
    ├── system_prompt.md     # LLM system prompt
    └── analysis_prompt.md   # Analysis prompt template
```

## Pipeline Flow

1. **URL Parsing** - Extract video ID from YouTube URL
2. **Transcript Fetch** - Get timestamped transcript via YouTube Transcript API
3. **Video Download** - Download MP4 to `downloads/` via yt-dlp
4. **Frame Extraction** - Extract 3 frames at even intervals using OpenCV
5. **Visual Analysis** - Analyze each frame with `llava` model (multimodal)
6. **Summary Generation** - Combine transcript + visual context, send to `llama3.2`
7. **Output** - Save markdown file and display in terminal

## Commands

```bash
# Setup
mise install                  # Install Python 3.14, Ollama, uv
uv venv && uv sync           # Create venv and install deps
uv pip install .             # Install CLI entry point

# Run
ytainotetaker "https://www.youtube.com/watch?v=VIDEO_ID"

# Output: {VIDEO_ID}_analysis.md in current directory
```

## Dependencies

- **ollama** - LLM inference client
- **opencv-python** - Video frame extraction
- **yt-dlp** - YouTube video download
- **youtube-transcript-api** - Transcript fetching
- **rich** - Terminal markdown rendering

## Runtime Requirements

- Ollama server running (`ollama serve`)
- Models pulled: `ollama pull llava` and `ollama pull llama3.2`
- `OLLAMA_HOST` env var (optional, defaults to localhost)

## Key Files

- `pyproject.toml` - Package config, CLI entry point defined as `ytainotetaker`
- `mise.toml` - Tool versions (Python 3.14, uv 0.9.22, Ollama 0.13.5)
- `instructions/*.md` - LLM prompts that define output structure

## Code Patterns

- Each subpackage exports via `__all__` in `__init__.py`
- Frames are base64-encoded for Ollama multimodal API
- Timestamps formatted as `[MM:SS]` or `[HH:MM:SS]`
- Visual context includes ±30 seconds of surrounding transcript
