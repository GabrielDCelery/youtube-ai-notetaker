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
├── segmentation/
│   └── detector.py          # Topic segmentation via LLM (llama3.1:8b)
├── analysis/
│   ├── ollama.py            # Ollama client configuration
│   ├── visual.py            # Frame analysis with llava model
│   └── summary.py           # Summary generation with llama3.2
├── utils/
│   └── formatter.py         # Timestamp formatting
└── instructions/
    ├── system_prompt.md     # LLM system prompt
    ├── analysis_prompt.md   # Analysis prompt template
    └── segmentation_prompt.md # Segmentation prompt template
```

## Pipeline Flow

1. **URL Parsing** - Extract video ID from YouTube URL
2. **Transcript Fetch** - Get timestamped transcript via YouTube Transcript API
3. **Topic Segmentation** - Analyze transcript with `llama3.1:8b` to identify distinct sections with timestamps
4. **Video Download** - Download MP4 to `downloads/` via yt-dlp
5. **Frame Extraction** - Extract frames (currently 3 at even intervals, planned: segment-aware)
6. **Visual Analysis** - Analyze each frame with `llava` model (multimodal)
7. **Summary Generation** - Combine transcript + visual context, send to `llama3.2`
8. **Output** - Save markdown file and display in terminal

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
- Models pulled: `ollama pull llava`, `ollama pull llama3.2`, and `ollama pull llama3.1:8b`
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

### Completed: Topic Segmentation

The segmentation module (`segmentation/detector.py`) is now implemented:
- `detect_segments()` analyzes transcript with `llama3.1:8b`
- Returns list of segments: `[{"topic": str, "start": float, "end": float}, ...]`
- Uses `segmentation_prompt.md` template with `[HH:MM:SS - HH:MM:SS] Topic name` format

### Next Steps

#### 1. Dynamic Frame Allocation (Not Yet Implemented)

Frame extraction still uses fixed 3-frame sampling. Needs update to:
- Extract frames proportional to segment length/importance
- Long technical sections get more frames
- Short intros/outros get fewer or none

#### 2. Section-Aware Visual Analysis (Not Yet Implemented)

Send llava frames grouped by segment with relevant transcript context instead of individual frame analysis.

#### 3. Analysis Modes (Not Yet Implemented)

Add CLI flags to support different use cases:

| Mode | Description | Use Case |
|------|-------------|----------|
| `--quick` | Transcript + segmentation only, no visuals | Fast overview, talking-head videos |
| `--full` | Transcript + segment-aware visual analysis | Tutorials with diagrams/code |

### Why This Architecture Matters

- **Efficiency** - Don't waste llava calls on segments without meaningful visuals
- **Quality** - llava gets better context when frames are grouped by topic
- **Scalability** - Handles 10-minute and 2-hour videos appropriately
- **Flexibility** - Quick mode for fast passes, full mode for comprehensive analysis
