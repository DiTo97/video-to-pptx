import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from video2pptx.base.video import VideoMetadata


@dataclass
class Downloader(ABC):
    """An abstract class that downloads videos and captions locally

    Notes
    -----
    The files are available only after being downloaded in their entirety.
    """
    proxies: typing.Dict[str, str] = None

    def __post_init__(self) -> None:
        if self.proxies is None:
            self.proxies = {}

    @abstractmethod
    def _download_caption(
        self, data: Any, output_dirpath: str, lang_code: str = "en"
        ) -> typing.Optional[str]:
        """It downloads the caption of a video in the given language to the given dirpath
        
        Returns
        -------
        The filepath to the saved caption or None

        Notes
        -----
        - The filename is the same as the video's with .srt extension.
        """
        pass

    @abstractmethod
    def _download_video(
        self, 
        url: str, 
        output_dirpath: str, 
        filename: typing.Optional[str] = None
    ) -> str:
        """It downloads the video at the given URL to the given dirpath

        Returns
        -------
        The filepath to the saved video

        Notes
        -----
        - If no filename is provided, it is randomly generated.
        """
        pass

    @abstractmethod
    def download(
        self, 
        src: str, 
        output_dirpath: str, 
        lang_code: str = "en", 
        filename: typing.Optional[str] = None
    ) -> VideoMetadata:
        """It downloads the video at the given src and its caption to the given dirpath

        Returns
        -------
        The downloaded video metadata

        Notes
        -----
        - The network call may use proxy servers to hide the IP address.
        """
        pass
