import typing
from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt


class BaseMotionFilter(ABC):
    """A base class that filters motionless consecutive frames from a sequence of frames

    The motion filter should minimize redundancy in the sequence of frames.
    In the case of scientific presentations, redundancy may occur with long explanations.
    """

    @abstractmethod
    def _detect_motion(
        self, frame1: npt.NDArray[np.uint8], frame2: npt.NDArray[np.uint8]
    ) -> bool:
        """It detects if there is significant motion between two frames"""

    @abstractmethod
    def filter_motionless_frames(
        self, frames_iter: typing.Iterator[npt.NDArray[np.uint8]]
    ) -> typing.Iterator[typing.Tuple[npt.NDArray[np.uint8], int]]:
        """It filters out motionless consecutive frames from an iterator of frames

        Two consecutive frames that show no significant motion, are compressed into a single frame.

        Returns
        -------
            A generator of compressed frames and the number of corresponding frames
        """
