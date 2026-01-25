from pathlib import Path

from ollama import Client

from youtube_ai_notetaker.segmentation.detector import Segment
from youtube_ai_notetaker.transcript.fetcher import TranscriptSnippet
from youtube_ai_notetaker.utils.formatter import format_timestamp

from .ollama import ollama_client

# Load prompts from instruction files
# Navigate up to project root: analysis -> youtube_ai_notetaker -> src -> project_root
INSTRUCTIONS_DIR = Path(__file__).parent.parent / "instructions"
ANALYSIS_PROMPT_TEMPLATE = (INSTRUCTIONS_DIR / "analysis_prompt.md").read_text()
SYSTEM_PROMPT = (INSTRUCTIONS_DIR / "system_prompt.md").read_text()
QUICK_SUMMARY_PROMPT = (INSTRUCTIONS_DIR / "quick_summary_prompt.md").read_text()


def generate_quick_summary(
    ollama_client: Client,
    transcript_snippets: list[TranscriptSnippet],
    segments: list[Segment],
) -> str:
    transcript_txt = format_transcript_snippets(transcript_snippets)
    segments_txt = format_segments(segments)
    prompt = QUICK_SUMMARY_PROMPT.format(
        transcript=transcript_txt, segments=segments_txt
    )

    response = ollama_client.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"] or ""


def generate_summary_with_diagrams(transcript, visual_context="") -> str | None:
    # Load and format the prompt template with actual data
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        transcript=transcript, visual_context=visual_context
    )

    response = ollama_client.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"]


def format_transcript_snippets(transcript_snippets: list[TranscriptSnippet]) -> str:
    return "\n".join(
        f"[{format_timestamp(s['start'])}] {s['text']}" for s in transcript_snippets
    )


def format_segments(segments: list[Segment]) -> str:
    return "\n".join(
        f"[{format_timestamp(s['start'])} - {format_timestamp(s['end'])}] {s['topic']}"
        for s in segments
    )
