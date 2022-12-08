import typing
from dataclasses import dataclass

import numpy.typing as npt
import srt

from video2pptx.base.pptx import BaseSlide


@dataclass
class BaseSynchronizer:
    """A base class that temporally aligns a sequence of frames and a sequence of subtitles
    
    The temporal alignment is controlled by a given frame rate.
    """
    frame_rate: int = 30

    def align(
        self, 
        frames_iter: typing.Iterator[npt.NDArray], 
        subtitles_iter: typing.Optional[typing.Iterator[srt.Subtitle]]
    ) -> typing.Iterator[BaseSlide]:
        """It temporally aligns a sequence of frames and a sequence of subtitles
        
        Returns
        -------
        A generator of (the contents of) PPTX slides
        """
        if subtitles_iter is not None:
            pass
        else:
            for frame in frames_iter:
                yield BaseSlide(frame, None)
