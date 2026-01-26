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
│   └── frames.py            # Frame extraction via OpenCV (segment-aware)
├── transcript/
│   └── fetcher.py           # YouTube transcript API
├── segmentation/
│   └── detector.py          # Topic segmentation via LLM (llama3.1:8b)
├── analysis/
│   ├── ollama.py            # Ollama client configuration
│   ├── visual.py            # Segment-aware visual analysis with llava
│   └── summary.py           # Summary generation (quick + full modes)
├── utils/
│   └── formatter.py         # Timestamp formatting
└── instructions/
    ├── system_prompt.md     # LLM system prompt
    ├── analysis_prompt.md   # Analysis prompt template
    ├── segmentation_prompt.md           # Segmentation prompt template
    ├── quick_summary_prompt.md          # Quick mode summary prompt
    └── segmentation_visual_context_prompt.md  # Visual-to-markdown conversion prompt
```

## Pipeline Flow

### Quick Mode (`--quick`, default)
1. **URL Parsing** - Extract video ID from YouTube URL
2. **Transcript Fetch** - Get timestamped transcript via YouTube Transcript API
3. **Topic Segmentation** - Analyze transcript with `llama3.1:8b` to identify distinct sections
4. **Summary Generation** - Generate summary from transcript + segments
5. **Output** - Save `{VIDEO_ID}_quick_summary.md` and display in terminal

### Full Mode (`--full`)
1. **URL Parsing** - Extract video ID from YouTube URL
2. **Transcript Fetch** - Get timestamped transcript via YouTube Transcript API
3. **Topic Segmentation** - Analyze transcript with `llama3.1:8b` to identify distinct sections
4. **Video Download** - Download MP4 via yt-dlp
5. **Segment-Aware Frame Extraction** - Extract fixed frames per segment (default: 2), seeking by timestamp
6. **Visual Analysis** - For each segment, send frames + transcript to `llava` to convert visuals to markdown (mermaid diagrams, code blocks, tables)
7. **Summary Generation** - Combine summarized discussion points + preserved visual content via `llama3.1:8b`
8. **Output** - Save `{VIDEO_ID}_full_analysis.md` and display in terminal

## Commands

```bash
# Setup
mise install                  # Install Python 3.14, Ollama, uv
uv venv && uv sync           # Create venv and install deps
uv pip install .             # Install CLI entry point

# Run - Quick mode (default)
ytainotetaker "https://www.youtube.com/watch?v=VIDEO_ID"

# Run - Full mode with visual analysis
ytainotetaker --mode full "https://www.youtube.com/watch?v=VIDEO_ID"

# With custom directories
ytainotetaker --mode full -d ./downloads -o ./output "https://www.youtube.com/watch?v=VIDEO_ID"
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

## Completed Features

### Topic Segmentation
- `detect_segments()` analyzes transcript with `llama3.1:8b`
- Returns list of segments: `[{"topic": str, "start": float, "end": float}, ...]`
- Uses `segmentation_prompt.md` template with `[HH:MM:SS - HH:MM:SS] Topic name` format

### Segment-Aware Frame Extraction
- `extract_frames_from_segments()` extracts fixed frames per segment
- Seeks by timestamp (`CAP_PROP_POS_MSEC`) for reliable positioning
- Frames compressed via JPEG quality + resize for smaller payloads
- Returns `[{"segment": {...}, "frames": [...]}, ...]`

### Segment-Aware Visual Analysis
- `analyze_segments_visual()` sends frames grouped by segment to llava
- Prompt instructs llava to **convert** visuals to markdown (mermaid, code blocks, tables)
- Not just descriptions - actual diagram reproduction

### Analysis Modes
| Mode | Flag | Description | Output |
|------|------|-------------|--------|
| Quick | `--quick` (default) | Transcript + segmentation only | `{VIDEO_ID}_quick_summary.md` |
| Full | `--full` | Transcript + segment-aware visual analysis | `{VIDEO_ID}_full_analysis.md` |

### Full Summary Generation
- Summarizes key discussion points (not verbatim transcript)
- Preserves mermaid diagrams, code blocks, ASCII art exactly
- Integrates transcript summary with visual content

## Future Direction

### Potential Improvements

- **Importance-based frame allocation** - Use LLM to score segments for visual importance, allocate more frames to diagram-heavy sections
- **Parallel segment analysis** - Process multiple segments concurrently for faster full analysis
- **Prompt tuning** - Improve mermaid syntax accuracy from llava output
- **Caching** - Cache downloaded videos and transcripts to avoid re-fetching
