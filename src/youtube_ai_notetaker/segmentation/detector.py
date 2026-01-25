import json
import re
from pathlib import Path
from typing import TypedDict

from ollama import Client

from youtube_ai_notetaker.transcript.fetcher import TranscriptSnippet
from youtube_ai_notetaker.utils.formatter import format_timestamp


class Segment(TypedDict):
    topic: str
    start: float
    end: float


INSTRUCTIONS_DIR = Path(__file__).parent.parent / "instructions"
SEGMENTATION_PROMPT = (INSTRUCTIONS_DIR / "segmentation_prompt.md").read_text()


def detect_segments(
    ollama_client: Client, transcript_snippets: list[TranscriptSnippet]
) -> list[Segment]:
    """
    Returns list of segments like:
    [{"topic": str, "start": float, "end": float}, ...]
    """
    duration = transcript_snippets[-1]["start"] + transcript_snippets[-1]["duration"]
    duration_formatted = format_timestamp(duration)
    transcript_txt = format_transcript_snippets(transcript_snippets)
    prompt = SEGMENTATION_PROMPT.format(
        transcript=transcript_txt, duration_formatted=duration_formatted
    )
    response = ollama_client.chat(
        # model="llama3.2",
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": "You are a transcript segmentation tool. You ONLY output segment lists in the format [HH:MM:SS - HH:MM:SS] Topic name. Never summarize or explain.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response["message"]["content"]
    segments = parse_segments_response(content)
    return segments


def format_transcript_snippets(transcript_snippets: list[TranscriptSnippet]) -> str:
    return "\n".join(
        f"[{format_timestamp(s['start'])}] {s['text']}" for s in transcript_snippets
    )


def parse_segments_response(response_text: str) -> list[Segment]:
    pattern = r"\[(\d+:\d+:\d+)\s*-\s*(\d+:\d+:\d+)\]\s*(.+)"
    segments: list[Segment] = []
    for match in re.finditer(pattern, response_text):
        start_str, end_str, topic = match.groups()
        segments.append(
            {
                "topic": topic.strip(),
                "start": timestamp_to_seconds(start_str),
                "end": timestamp_to_seconds(end_str),
            }
        )
    return segments


def timestamp_to_seconds(ts: str) -> float:
    parts = ts.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    # HH:MM:SS
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
