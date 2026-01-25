from pathlib import Path

import yt_dlp


def download_video(download_dir: str, url: str, video_id: str) -> str:
    output_filename = f"video_{video_id}.mp4"
    output_path = str(Path(download_dir) / output_filename)
    with yt_dlp.YoutubeDL(
        {
            "format": "best[ext=mp4]",
            "outtmpl": output_path,
        }
    ) as ydl:
        ydl.download([url])
    return output_path
