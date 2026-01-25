"""YouTube AI Notetaker"""

__version__ = "0.1.0"

from youtube_ai_notetaker.analysis import (
    analyze_video_content,
    generate_quick_summary,
    generate_summary_with_diagrams,
)
from youtube_ai_notetaker.segmentation import detect_segments
from youtube_ai_notetaker.settings import parse_arguments
from youtube_ai_notetaker.transcript import get_transcript, get_transcript_snipttets
from youtube_ai_notetaker.video import download_video, extract_frames, get_video_id

__all__ = [
    "get_video_id",
    "detect_segments",
    "download_video",
    "extract_frames",
    "get_transcript",
    "analyze_video_content",
    "generate_summary_with_diagrams",
    "parse_arguments",
    "get_transcript_snipttets",
    "generate_quick_summary",
]
