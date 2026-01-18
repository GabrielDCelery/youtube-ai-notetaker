import base64
import os
import re
from pathlib import Path

import cv2
import ollama
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

ollama_host = os.getenv("OLLAMA_HOST", "localhost")

# Configure Ollama client to use remote host
ollama_client = ollama.Client(host=f"{ollama_host}:11434")

# Load prompts from instruction files
INSTRUCTIONS_DIR = Path(__file__).parent / "instructions"
ANALYSIS_PROMPT_TEMPLATE = (INSTRUCTIONS_DIR / "analysis_prompt.md").read_text()
SYSTEM_PROMPT = (INSTRUCTIONS_DIR / "system_prompt.md").read_text()


def get_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    # Return both formatted text with timestamps and raw snippets
    formatted_parts = []
    for snippet in transcript.snippets:
        timestamp = format_timestamp(snippet.start)
        formatted_parts.append(f"[{timestamp}] {snippet.text}")
    return "\n".join(formatted_parts), transcript.snippets


def format_timestamp(seconds):
    """Convert seconds to MM:SS or HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def download_video(url: str, video_id: str) -> str:
    output_dir = "downloads"
    output_filename = f"video_{video_id}.mp4"
    output_path = f"{output_dir}/{output_filename}"
    with yt_dlp.YoutubeDL(
        {
            "format": "best[ext=mp4]",
            "outtmpl": output_path,
        }
    ) as ydl:
        ydl.download([url])
    return output_path


def extract_frames(video_path, num_frames=5) -> list[dict]:
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
    frames: list[dict] = []
    for idx in frames_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            _, buffer = cv2.imencode(".jpg", frame)
            timestamp_seconds = idx / fps if fps > 0 else 0
            frames.append(
                {
                    "timestamp": timestamp_seconds,
                    "timestamp_formatted": format_timestamp(timestamp_seconds),
                    "frame_index": idx,
                    "image": base64.b64encode(buffer).decode("utf-8"),
                }
            )
    cap.release()
    return frames


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
