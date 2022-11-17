import typing
from dataclasses import dataclass

import cv2
import numpy.typing as npt
import srt

from video2pptx.base.video import BaseVideoMetadata
from video2pptx.utils.sampling import sample_linspace


def extract_frames_from_capture(capture: cv2.VideoCapture) -> typing.Iterator[npt.NDArray]:
    """It extracts frames from an OpenCV video capture"""
    num_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    num_read_frames = 0

    while True:
        status, frame = capture.read()

        if not status:
            if num_read_frames != num_frames:
                raise ValueError(
                    "The capture has stopped before reading all frames"
                )

            break

        yield frame
        num_read_frames += 1


def sample_frames_by_frame_rate(
    frames_iter: typing.Iterator[npt.NDArray], 
    frame_rate: int, 
    desired_frame_rate: int
) -> typing.Iterator[npt.NDArray]:
    """It samples from a sequence of frames by the given desired frame rate"""
    if desired_frame_rate > frame_rate:
        raise ValueError(
            "The desired frame rate must be \le than the frame rate"
        )

    frames_in_sec = []

    for frame in frames_iter:
        frames_in_sec.append(frame)

        if len(frames_in_sec) == frame_rate:
            if desired_frame_rate < frame_rate:
                frames_in_sec = sample_linspace(
                    frames_in_sec, frame_rate, desired_frame_rate
                )

            for frame in frames_in_sec:
                yield frame

            frames_in_sec = []

    # If frame_rate is not divisible by desired_frame_rate,
    # there will be some frames left over in the last sec batch
    if frames_in_sec:
        if desired_frame_rate < frame_rate:
            frames_in_sec = sample_linspace(
                frames_in_sec, frame_rate, desired_frame_rate
            )

        for frame in frames_in_sec:
            yield frame


@dataclass
class BaseExtractor:
    """A base class that extracts frames from a video and subtitles from a caption
    
    The extraction is controlled by a given frame rate.
    """
    frame_rate: int = 30

    def _extract_frames(self, filepath: str) -> typing.Iterator[npt.NDArray]:
        """It extracts frames from a video at the given path

        The frame rate is capped at the original frame rate of the video.
        
        Returns
        -------
        A generator of frames
        """
        capture = cv2.VideoCapture(filepath)

        if not capture.isOpened():
            raise ValueError(f"Unable to open {filepath}")

        capture_frame_rate = round(capture.get(cv2.CAP_PROP_FPS))
        frame_rate = min(self.frame_rate, capture_frame_rate)

        frames_iter = extract_frames_from_capture(capture)

        sampled_frames_iter = sample_frames_by_frame_rate(
            frames_iter, capture_frame_rate, frame_rate
        )

        for frame in sampled_frames_iter:
            yield frame

        capture.release()

    def _extract_subtitles(self, caption_filepath: str) -> typing.Iterator[srt.Subtitle]:
        """It extracts subtitles from the caption of a video at the given path
        
        Returns
        -------
        A generator of subtitles
        """
        with open(caption_filepath, "rt") as f:
            srt_data = f.read()

        return srt.parse(srt_data)

    def extract(
        self, metadata: BaseVideoMetadata
    ) -> typing.Tuple[
        typing.Iterator[npt.NDArray], 
        typing.Optional[typing.Iterator[srt.Subtitle]]
    ]:
        """It extracts frames and subtitles from a video metadata
        
        Returns
        -------
        A generator of frames and subtitles (or None)
        """
        filepath = metadata.filepath
        caption_filepath = metadata.caption_filepath

        frames = self._extract_frames(filepath)
        
        subtitles = (
            None if caption_filepath is None 
            else self._extract_subtitles(caption_filepath)
        )

        return frames, subtitles
