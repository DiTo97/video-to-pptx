import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from video2pptx.base.datamodels.video import BaseVideoMetadata
from video2pptx.utils.typing import strOrPath


@dataclass
class BaseDownloader(ABC):
    """An abstract class that downloads videos from local or remote data sources

    Notes
    -----
    - The files are available only after being downloaded in their entirety.
    """

    @abstractmethod
    def download(
        self,
        data_src: strOrPath,
        output_dirpath: strOrPath,
        filename: typing.Optional[strOrPath] = None,
    ) -> BaseVideoMetadata:
        """It downloads the video at the given data source to the given dirpath

        Returns
        -------
            The downloaded video metadata
        """
