import argparse
from pathlib import Path

from rich import markdown, print

from youtube_ai_notetaker.analysis import (
    analyze_video_content,
    generate_summary_with_diagrams,
)
from youtube_ai_notetaker.transcript import get_transcript
from youtube_ai_notetaker.video import download_video, get_video_id


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI-powered notes from YouTube videos"
    )
    parser.add_argument("url", help="YouTube video URL")
    # parser.add_argument(
    #     "--frames", type=int, default=3, help="Number of frames to analyze (default: 3)"
    # )
    # parser.add_argument(
    #     "--output", help="Output file path (default: <video_id>_analysis.md)"
    # )

    args = parser.parse_args()

    video_id = get_video_id(args.url)
    if not video_id:
        print("[red] Invalid YouTube URL[/red]")
        return
    print("get transcript")
    transcript_text, transcript_snippets = get_transcript(video_id)
    print("download video")
    video_path = download_video(args.url, video_id)
    print("analyze video content")
    visual_context = analyze_video_content(video_path, transcript_snippets)
    print("generate summary with diagrams")
    analysis = generate_summary_with_diagrams(transcript_text, visual_context)
    if analysis is None:
        print("[red] no analysis result[/red]")
        return

    # Write to markdown file
    output_file = Path(f"{video_id}_analysis.md")
    output_file.write_text(analysis)
    print(f"[green]Analysis saved to {output_file}[/green]\n")

    # Print to console
    print(markdown.Markdown(markup=analysis))


if __name__ == "__main__":
    main()
