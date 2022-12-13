import typing
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
import srt

from video2pptx.base.datamodels.pptx import BaseSlide


@dataclass
class BaseSynchronizer:
    """A base class that temporally aligns a sequence of frames and a sequence of subtitles

    The temporal alignment is controlled by a given frame rate.
    """

    frame_rate: int = 30

    def synchronize(
        self,
        frames_iter: typing.Iterator[typing.Tuple[npt.NDArray[np.uint8], int]],
        subtitles_iter: typing.Optional[typing.Iterator[srt.Subtitle]],
    ) -> typing.Iterator[BaseSlide]:
        """It temporally aligns a sequence of frames and a sequence of subtitles

        Returns
        -------
            A generator of (the contents of) PPTX slides
        """
        for frame, _ in frames_iter:
            if subtitles_iter is not None:
                pass

            yield BaseSlide(frame, None)
