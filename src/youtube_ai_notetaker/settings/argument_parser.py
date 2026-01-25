import argparse


class Args(argparse.Namespace):
    video_url: str
    download_dir: str
    output_dir: str
    ollama_host: str


def parse_arguments() -> Args:
    parser = argparse.ArgumentParser(
        description="Generate AI-powered notes from YouTube videos"
    )

    parser.add_argument("video_url", help="YouTube video URL")
    parser.add_argument(
        "-d", "--download_dir", help="The location to download the YouTube videos"
    )
    parser.add_argument(
        "-o", "--output_dir", help="The dir to output the results of the analysis"
    )
    parser.add_argument(
        "-H",
        "--ollama_host",
        help="Ollama host (default: http://localhost:11434)",
        default="http://localhost:11434",
    )

    # parser.add_argument(
    #     "--frames", type=int, default=3, help="Number of frames to analyze (default: 3)"
    # )
    # parser.add_argument(
    #     "--output", help="Output file path (default: <video_id>_analysis.md)"
    # )

    ns = parser.parse_args()

    return Args(
        video_url=ns.video_url,
        download_dir=ns.download_dir,
        output_dir=ns.output_dir,
        ollama_host=ns.ollama_host,
    )
