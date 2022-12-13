import typing
from abc import ABC, abstractmethod

from pptx import presentation

from video2pptx.base.datamodels.pptx import BaseSlide


class BaseBuilder(ABC):
    """An abstract class that builds PPTX presentations from temporally aligned contents"""

    @abstractmethod
    def build(
        self, slides_iter: typing.Iterator[BaseSlide]
    ) -> presentation.Presentation:
        ...
