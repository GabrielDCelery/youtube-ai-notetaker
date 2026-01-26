import base64
from typing import TypedDict

import cv2

from youtube_ai_notetaker.segmentation.detector import Segment
from youtube_ai_notetaker.utils import format_timestamp

# https://www.geeksforgeeks.org/python/how-to-get-properties-of-python-cv2-videocapture-object/


class Frame(TypedDict):
    timestamp: float
    frame_index: int
    image: str


class SegmentWithFrames(TypedDict):
    segment: Segment
    frames: list[Frame]


def extract_frames_from_segments(
    video_path: str, segments: list[Segment], frames_per_segment: int = 2
) -> list[SegmentWithFrames]:
    """
    Extract frames for each segment.

    Returns: [
        {
            "segment": {"topic": str, "start": float, "end": float},
            "frames": [{"timestamp": float, "frame_index": int, "image": str}, ...]
        },
        ...
    ]
    """
    segments_with_frames: list[SegmentWithFrames] = []
    capture = cv2.VideoCapture(video_path)
    fps = capture.get(cv2.CAP_PROP_FPS)  # get the number of frames per second
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / fps if fps > 0 else 0
    print(f"Video: fps={fps}, total_frames={total_frames}, duration={video_duration}s")
    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        duration = end - start
        frames: list[Frame] = []
        for i in range(frames_per_segment):
            timestamp = start + (i + 0.5) * (duration / frames_per_segment)
            frame_index = int(timestamp * fps)
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            # capture.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            exists, frame = capture.read()
            if not exists:
                continue
            max_width = 720
            height, width = frame.shape[:2]
            if width > max_width:
                scale = max_width / width
                frame = cv2.resize(frame, (max_width, int(height * scale)))
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, 60]
            _, buffer = cv2.imencode(".jpg", frame, encode_params)
            frames.append(
                {
                    "timestamp": timestamp,
                    "frame_index": frame_index,
                    "image": base64.b64encode(buffer).decode("utf-8"),
                }
            )
        segments_with_frames.append({"segment": segment, "frames": frames})
    capture.release()
    return segments_with_frames


def extract_frames(video_path, num_frames=5) -> list[dict]:
    capture = cv2.VideoCapture(video_path)
    # CAP_PROP_FRAME_COUNT
    # Total number of frame: This property is used to calculate the total number of frames in the video file.
    # CAP_PROP_FPS
    # FPS stands for frames per second. This property is used to get the frame rate of the video.
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = capture.get(cv2.CAP_PROP_FPS)
    frames_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
    frames: list[dict] = []
    for idx in frames_indices:
        capture.set(cv2.CAP_PROP_POS_FRAMES, idx)
        # grab, decode and return the next video frame
        ret, frame = capture.read()
        if ret:
            # encode the frame into a memory buffer
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
    capture.release()
    return frames
