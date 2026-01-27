# CLAUDE.md

## Project Overview

CLI tool that generates markdown notes from YouTube videos using local LLMs via Ollama.

## Architecture

```
src/youtube_ai_notetaker/
├── cli.py                    # Entry point - ytainotetaker command
├── video/                    # URL parsing, download (yt-dlp), frame extraction (OpenCV)
├── transcript/fetcher.py     # YouTube transcript API
├── segmentation/detector.py  # Topic segmentation via llama3.1:8b
├── analysis/                 # Ollama client, visual analysis (llava), summary generation
├── utils/formatter.py        # Timestamp formatting
└── instructions/*.md         # LLM prompt templates
```

## Code Patterns

- Subpackages export via `__all__` in `__init__.py`
- Frames base64-encoded for Ollama multimodal API
- Timestamps: `[MM:SS]` or `[HH:MM:SS]`
- Use `pathlib.Path` for file paths
- Typed args via `Args(argparse.Namespace)` class
