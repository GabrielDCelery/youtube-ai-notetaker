from pathlib import Path

from ollama import Client

from youtube_ai_notetaker.analysis.visual import SegmentVisualAnalysis
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


def generate_full_summary(
    ollama_client: Client, analyzed_segments: list[SegmentVisualAnalysis]
) -> str:
    """
    Generate a cohesive markdown summary from analyzed segments.
    """
    segments_context = ""
    for seg in analyzed_segments:
        segment = seg["segment"]
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        segments_context += f"""
## [{start} - {end}] {segment["topic"]}

**Transcript:**
{seg["transcript"]}

**Visual observations:**
{seg["visual"] or "No visual analysis available."}

---
"""

    prompt = f"""You are creating comprehensive markdown notes from a video analysis.

Below are segments from the video, each with transcript text and visual content (diagrams, code, etc.) extracted from key frames.

{segments_context}

Create a well-structured markdown document that:
1. Has a clear title and overview
2. Organizes information by topic/segment
3. Integrates transcript content with the visual content
4. Highlights key takeaways and important details
5. Uses proper markdown formatting (headers, lists, code blocks if relevant)

IMPORTANT: Preserve all mermaid diagrams, code blocks, ASCII art, and markdown tables from the visual content EXACTLY as they appear. Do not summarize or describe them - include them directly in your output.

Write the complete markdown document:"""

    response = ollama_client.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
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
