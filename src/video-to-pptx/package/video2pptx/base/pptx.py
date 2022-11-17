import typing
from dataclasses import dataclass

import srt
import numpy.typing as npt


@dataclass
class BaseSlide:
    """A base class that implements a PPTX slide
    
    A PPTX slide has a frame and may have a subtitle
    """
    frame: npt.NDArray
    subtitle: typing.Optional[srt.Subtitle]
