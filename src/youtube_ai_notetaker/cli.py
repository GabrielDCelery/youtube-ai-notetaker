from pathlib import Path

import ollama
from rich import markdown, print

from youtube_ai_notetaker import (
    analyze_video_content,
    download_video,
    generate_summary_with_diagrams,
    get_transcript,
    get_transcript_snipttets,
    get_video_id,
    parse_arguments,
)
from youtube_ai_notetaker.segmentation.detector import detect_segments


def main():
    args = parse_arguments()

    ollama_client = ollama.Client(host=args.ollama_host)

    video_id = get_video_id(args.video_url)

    if not video_id:
        print("[red] Invalid YouTube URL[/red]")
        return

    print(f"get transcript for video {video_id}")
    transcript_snippets = get_transcript_snipttets(video_id)

    print(f"detect segments from transcript")
    segments = detect_segments(ollama_client, transcript_snippets)

    print(segments)

    # print(f"download video {video_id}")
    # video_path = download_video(args.download_dir, args.video_url, video_id)
    #
    # print("analyze video content")
    # visual_context = analyze_video_content(video_path, transcript_snippets)
    #
    # print("generate summary with diagrams")
    # analysis = generate_summary_with_diagrams(transcript_text, visual_context)
    #
    # if analysis is None:
    #     print("[red] no analysis result[/red]")
    #     return
    #
    # # Write to markdown file
    # output_file = Path("downloads", f"{video_id}_analysis.md")
    # output_file.write_text(analysis)
    # print(f"[green]Analysis saved to {output_file}[/green]\n")
    #
    # # Print to console
    # print(markdown.Markdown(markup=analysis))


if __name__ == "__main__":
    main()
