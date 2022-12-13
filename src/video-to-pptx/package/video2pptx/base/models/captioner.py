import pathlib
import typing
from abc import ABC, abstractmethod

import srt

from video2pptx.base.datamodels.video import BaseVideoMetadata


class BaseCaptioner(ABC):
    """An abstract class that computes captions from videos

    Notes
    -----
    - 'To captionify' is a short form for 'To compute captions'
    """

    @abstractmethod
    def captionify(self, filepath: pathlib.Path) -> typing.Iterator[srt.Subtitle]:
        ...

    def from_metadata(self, metadata: BaseVideoMetadata) -> BaseVideoMetadata:
        if metadata.caption_filepath is not None:
            return metadata

        filepath = metadata.filepath

        subtitles_iter = self.captionify(filepath)
        caption = srt.compose(subtitles_iter)

        caption_filepath = filepath.with_suffix(".srt")

        with caption_filepath.open("wt") as f:
            f.write(caption)

        metadata.caption_filepath = caption_filepath
        return metadata
