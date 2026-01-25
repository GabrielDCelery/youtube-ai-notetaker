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
- Use `pathlib.Path` for file path construction
- Typed argument parsing via custom `Args(argparse.Namespace)` class

## Future Direction

### Problem with Current Approach

The current pipeline extracts a fixed number of frames (3) at even intervals. This works poorly for:
- **Long videos** (1-2 hours) - 3 frames can't capture enough content
- **Uneven content distribution** - A 2-hour talk might have diagrams clustered in one section
- **Wasted processing** - Intro/outro segments get frames but have no useful visuals

### Planned Architecture: Segment-Aware Analysis

Instead of blind frame sampling, use a two-phase approach:

1. **Topic Segmentation** - Analyze transcript with LLM to identify distinct sections with timestamps
   ```json
   [
     {"topic": "Introduction", "start": 0, "end": 45},
     {"topic": "Setting up the project", "start": 45, "end": 312},
     {"topic": "Authentication deep-dive", "start": 312, "end": 1100}
   ]
   ```

2. **Dynamic Frame Allocation** - Extract frames proportional to section length/importance
   - Long technical sections get more frames
   - Short intros/outros get fewer or none

3. **Section-Aware Visual Analysis** - Send llava frames grouped by section with relevant transcript context

### Analysis Modes

Add CLI flags to support different use cases:

| Mode | Description | Use Case |
|------|-------------|----------|
| `--quick` | Transcript + segmentation only, no visuals | Fast overview, talking-head videos |
| `--full` | Transcript + segment-aware visual analysis | Tutorials with diagrams/code |

The segmentation step becomes the foundation for both modes - it improves summary structure even without visual analysis.

### Why This Matters

- **Efficiency** - Don't waste llava calls on segments without meaningful visuals
- **Quality** - llava gets better context when frames are grouped by topic
- **Scalability** - Handles 10-minute and 2-hour videos appropriately
- **Flexibility** - Quick mode for fast passes, full mode for comprehensive analysis
