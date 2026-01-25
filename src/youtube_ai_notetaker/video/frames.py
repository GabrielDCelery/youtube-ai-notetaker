import base64

import cv2

from youtube_ai_notetaker.utils import format_timestamp

# https://www.geeksforgeeks.org/python/how-to-get-properties-of-python-cv2-videocapture-object/


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
