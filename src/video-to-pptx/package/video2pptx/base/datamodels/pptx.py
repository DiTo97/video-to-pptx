import typing
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
import srt


@dataclass
class BaseSlide:
    """A base class that implements a PPTX slide

    A PPTX slide has a frame and may have a subtitle
    """

    frame: npt.NDArray[np.uint8]
    subtitle: typing.Optional[srt.Subtitle]
