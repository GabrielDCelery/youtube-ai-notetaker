from typing import TypedDict

from youtube_transcript_api import YouTubeTranscriptApi

from youtube_ai_notetaker.utils import format_timestamp


class TranscriptSnippet(TypedDict):
    start: float
    duration: float
    text: str


def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    # Return both formatted text with timestamps and raw snippets
    formatted_parts = []
    for snippet in transcript.snippets:
        timestamp = format_timestamp(snippet.start)
        formatted_parts.append(f"[{timestamp}] {snippet.text}")
    return "\n".join(formatted_parts), transcript.snippets


def get_transcript_snipttets(video_id: str) -> list[TranscriptSnippet]:
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    return [
        {"start": s.start, "duration": s.duration, "text": s.text}
        for s in transcript.snippets
    ]
