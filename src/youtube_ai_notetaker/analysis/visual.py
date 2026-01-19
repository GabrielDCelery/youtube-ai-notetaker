from youtube_ai_notetaker.video import extract_frames

from .ollama import ollama_client


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
