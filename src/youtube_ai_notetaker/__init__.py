"""YouTube AI Notetaker"""

__version__ = "0.1.0"

from youtube_ai_notetaker.analysis import (
    analyze_video_content,
    generate_summary_with_diagrams,
)
from youtube_ai_notetaker.transcript import get_transcript
from youtube_ai_notetaker.video import download_video, extract_frames, get_video_id

__all__ = [
    "get_video_id",
    "download_video",
    "extract_frames",
    "get_transcript",
    "analyze_video_content",
    "generate_summary_with_diagrams",
]
