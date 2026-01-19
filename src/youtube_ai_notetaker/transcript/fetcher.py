from youtube_transcript_api import YouTubeTranscriptApi

from youtube_ai_notetaker.utils import format_timestamp


def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    # Return both formatted text with timestamps and raw snippets
    formatted_parts = []
    for snippet in transcript.snippets:
        timestamp = format_timestamp(snippet.start)
        formatted_parts.append(f"[{timestamp}] {snippet.text}")
    return "\n".join(formatted_parts), transcript.snippets
