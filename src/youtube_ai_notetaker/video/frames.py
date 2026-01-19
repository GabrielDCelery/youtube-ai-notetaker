import base64

import cv2

from youtube_ai_notetaker.utils import format_timestamp


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
