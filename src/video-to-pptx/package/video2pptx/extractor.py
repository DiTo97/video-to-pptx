import typing

import cv2
import numpy as np
import numpy.typing as npt
import srt

from video2pptx.video.video import VideoMetadata


def _extract_frames(filepath: str, frame_rate: int = 30) -> typing.Iterator[npt.NDArray]:
    """It extracts frames from a video at the given path at the given frame rate

    The frame rate is capped at the original frame rate of the video.
    
    Returns
    -------
    A generator of frames
    """
    capture = cv2.VideoCapture(filepath)

    if not capture.isOpened():
        raise ValueError(f"Unable to open {filepath}")

    capture_frame_rate = round(capture.get(cv2.CAP_PROP_FPS))
    frame_rate = min(frame_rate, capture_frame_rate)

    finished = False

    while finished is False:
        frames_in_sec = []

        while True:
            idx = capture.get(cv2.CAP_PROP_POS_FRAMES) + 1
            status, frame = capture.read()

            if not status:
                finished = True
                break

            frames_in_sec.append(frame)

            if idx % capture_frame_rate == 0:
                break

        if frame_rate < capture_frame_rate:
            selected = np.linspace(0, capture_frame_rate - 1, frame_rate)
            selected = np.round(selected).astype(int)

            frames_in_sec = [
                frame for idx, frame in enumerate(frames_in_sec) if idx in selected
            ]

        for frame in frames_in_sec:
            yield frame

    capture.release()


def _extract_subtitles(caption_filepath: str) -> typing.Iterator[srt.Subtitle]:
    """It extracts subtitles from the caption of a video at the given path
    
    Returns
    -------
    A generator of subtitles
    """
    with open(caption_filepath, "rt") as f:
        srt_data = f.read()

    return srt.parse(srt_data)


def extract(
    metadata: VideoMetadata, frame_rate: int = 30
) -> typing.Tuple[
    typing.Iterator[npt.NDArray], 
    typing.Optional[typing.Iterator[srt.Subtitle]]
]:
    """It extracts frames and subtitles from a video metadata at the given frame rate
    
    Returns
    -------
    A generator of frames and subtitles (or None)
    """
    filepath = metadata.filepath
    caption_filepath = metadata.caption_filepath

    frames = _extract_frames(filepath, frame_rate)
    subtitles = None

    if caption_filepath is not None:
        subtitles = _extract_subtitles(caption_filepath)

    return frames, subtitles
