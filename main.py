import sys
from pathlib import Path

from rich import markdown, print

from downloader import (
    analyze_video_content,
    download_video,
    generate_summary_with_diagrams,
    get_transcript,
    get_video_id,
)


def main(youtube_url):
    video_id = get_video_id(youtube_url)
    if not video_id:
        print("[red] Invalid YouTube URL[/red]")
        return
    print("get transcript")
    transcript_text, transcript_snippets = get_transcript(video_id)
    print("download video")
    video_path = download_video(youtube_url, video_id)
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
    if len(sys.argv) < 2:
        print("Usage: pyton main.py <youtube_url>")
        sys.exit(1)
    main(sys.argv[1])
