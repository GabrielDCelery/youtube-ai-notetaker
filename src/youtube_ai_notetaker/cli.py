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
from youtube_ai_notetaker.analysis.summary import generate_quick_summary
from youtube_ai_notetaker.analysis.visual import analyze_segments_visual
from youtube_ai_notetaker.segmentation.detector import detect_segments
from youtube_ai_notetaker.video.frames import extract_frames_from_segments


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

    if args.mode == "quick":
        print(f"generating quick summary")
        quick_summary = generate_quick_summary(
            ollama_client, transcript_snippets, segments
        )
        output_file = Path(args.output_dir or ".", f"{video_id}_quick_summary.md")
        output_file.write_text(quick_summary)
        print(f"[green]Analysis saved to {output_file}[/green]\n")
        print(markdown.Markdown(markup=quick_summary))

    if args.mode == "full":
        print(f"download video {video_id}")
        video_path = download_video(args.download_dir, args.video_url, video_id)

        print(f"extract frames from video {video_path}")
        segments_with_frames = extract_frames_from_segments(video_path, segments, 10)

        visual_analysis = analyze_segments_visual(
            ollama_client, segments_with_frames, transcript_snippets
        )
        print(visual_analysis)

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
