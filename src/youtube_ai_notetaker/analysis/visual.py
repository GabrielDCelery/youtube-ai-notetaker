from pathlib import Path
from typing import TypedDict

from ollama import Client

from youtube_ai_notetaker.segmentation.detector import Segment
from youtube_ai_notetaker.transcript.fetcher import TranscriptSnippet
from youtube_ai_notetaker.video import extract_frames
from youtube_ai_notetaker.video.frames import SegmentWithFrames

from .ollama import ollama_client


class SegmentVisualAnalysis(TypedDict):
    segment: Segment
    transcript: str
    visual: str


INSTRUCTIONS_DIR = Path(__file__).parent.parent / "instructions"
SEGMENTATION_PROMPT = (
    INSTRUCTIONS_DIR / "segmentation_visual_context_prompt.md"
).read_text()


def analyze_segments_visual(
    ollama_client: Client,
    segments_with_frames: list[SegmentWithFrames],
    transcript_snippets: list[TranscriptSnippet],
) -> list[SegmentVisualAnalysis]:
    result: list[SegmentVisualAnalysis] = []
    for segment_data in segments_with_frames:
        segment = segment_data["segment"]
        frames = segment_data["frames"]
        segment_transcripts = [
            ts
            for ts in transcript_snippets
            if ts["start"] >= segment["start"]
            and (ts["start"] + ts["duration"]) <= segment["end"]
        ]
        transcript_text = " ".join(s["text"] for s in segment_transcripts)
        if not frames:
            result.append(
                {"segment": segment, "transcript": transcript_text, "visual": ""}
            )
            continue

        prompt = SEGMENTATION_PROMPT.format(
            transcript_text=transcript_text, topic=segment["topic"]
        )
        images = [f["image"] for f in frames]
        response = ollama_client.chat(
            model="llava",
            messages=[{"role": "user", "content": prompt, "images": images}],
        )
        result.append(
            {
                "segment": segment,
                "transcript": transcript_text,
                "visual": response["message"]["content"],
            }
        )
    return result


def analyze_video_content(video_path, transcript_snippets):
    frames = extract_frames(video_path, num_frames=3)

    # Get relevant transcript context for each frame
    visual_context = []
    for frame_data in frames:
        timestamp = frame_data["timestamp"]
        timestamp_formatted = frame_data["timestamp_formatted"]

        # Find transcript snippets around this timestamp (±30 seconds)
        context_snippets = [
            snippet
            for snippet in transcript_snippets
            if abs(snippet.start - timestamp) <= 30
        ]
        context_text = " ".join(
            [s.text for s in context_snippets[:5]]
        )  # Limit to 5 snippets

        prompt = f"""Analyze this video frame taken at timestamp {timestamp_formatted}.

Context from transcript around this time:
"{context_text}"

Describe:
1. Visual elements (charts, diagrams, code, presentations)
2. Key concepts shown visually
3. How the visuals relate to what's being discussed
Keep it concise but specific."""

        response = ollama_client.chat(
            model="llava",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [frame_data["image"]],
                }
            ],
        )
        visual_context.append(
            f"[{timestamp_formatted}] {response['message']['content']}"
        )
    return "\n\n".join(visual_context)
