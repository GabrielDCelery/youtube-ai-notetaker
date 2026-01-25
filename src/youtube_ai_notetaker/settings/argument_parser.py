import argparse
from typing import Literal


class Args(argparse.Namespace):
    video_url: str
    download_dir: str
    output_dir: str
    ollama_host: str
    mode: Literal["quick", "full"]


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

    parser.add_argument(
        "-m",
        "--mode",
        choices=["quick", "full"],
        default="quick",
        help="Analysis mode: 'quick' for transcript + segmentation only, 'full' for visual analysis (default: quick)",
    )

    ns = parser.parse_args()

    return Args(
        video_url=ns.video_url,
        download_dir=ns.download_dir,
        output_dir=ns.output_dir,
        ollama_host=ns.ollama_host,
        mode=ns.mode,
    )
