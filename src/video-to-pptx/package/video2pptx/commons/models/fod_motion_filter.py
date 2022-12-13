import typing
from dataclasses import dataclass

import cv2
import numpy as np
import numpy.typing as npt

from video2pptx.base.models import BaseMotionFilter


@dataclass
class FODMotionFilter(BaseMotionFilter):
    """A class that filters motionless consecutive frames by looking
    at 1st order differentiation (FOD)"""

    blurring_ksize: typing.Tuple[int, int] = (5, 5)
    dilation_ksize: typing.Tuple[int, int] = (5, 5)
    threshold: int = 30
    min_contour_area: int = 100

    def _detect_motion(
        self, frame1: npt.NDArray[np.uint8], frame2: npt.NDArray[np.uint8]
    ) -> bool:
        """It detects if there is significant motion between two frames

        The motion is approximated by 1st order differentiation on grayscale frames.
        """
        grayscale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        grayscale1 = cv2.GaussianBlur(grayscale1, self.blurring_ksize, 0)

        grayscale2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        grayscale2 = cv2.GaussianBlur(grayscale2, self.blurring_ksize, 0)

        dilation_kernel = np.ones(self.dilation_ksize)

        difference = cv2.absdiff(grayscale1, grayscale2)
        difference = cv2.dilate(difference, dilation_kernel, 1)

        _, thresholded = cv2.threshold(
            difference, self.threshold, 255, cv2.THRESH_BINARY
        )

        contours, _ = cv2.findContours(
            thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        return any(
            cv2.contourArea(contour) >= self.min_contour_area for contour in contours
        )

    def filter_motionless_frames(
        self, frames_iter: typing.Iterator[npt.NDArray[np.uint8]]
    ) -> typing.Iterator[typing.Tuple[npt.NDArray[np.uint8], int]]:
        """It filters out motionless consecutive frames from an iterator of frames

        Two consecutive frames that show no significant motion, are compressed into a single frame.

        Returns
        -------
            A generator of compressed frames and the number of corresponding frames
        """
        frame_tm1 = None
        num_corresponding = 0

        for frame in frames_iter:
            if frame_tm1 is None:
                frame_tm1 = frame
                num_corresponding = 1

                continue

            if self._detect_motion(frame_tm1, frame):
                yield frame_tm1, num_corresponding

                frame_tm1 = frame
                num_corresponding = 1

                continue

            num_corresponding += 1

        yield frame_tm1, num_corresponding
