from dataclasses import dataclass
from typing import Any

from video2pptx.base.models import (
    BaseBuilder,
    BaseCaptioner,
    BaseDownloader,
    BaseExtractor,
    BaseMotionFilter,
    BaseSynchronizer,
)
from video2pptx.utils.typing import strOrPath


@dataclass
class Pipeline:
    """A callable pipeline that converts videos to PPTX presentations"""

    builder: BaseBuilder
    captioner: BaseCaptioner
    downloader: BaseDownloader
    extractor: BaseExtractor
    motion_filter: BaseMotionFilter
    synchronizer: BaseSynchronizer

    def __call__(
        self,
        data_src: strOrPath,
        output_dirpath: strOrPath,
        filename: strOrPath,
        verbose: bool = False,
    ) -> None:
        metadata = self.downloader.download(data_src, output_dirpath, filename)
        metadata = self.captioner.from_metadata(metadata)

        frames_iter, subtitles_iter = self.extractor.extract(metadata)
        frames_iter = self.motion_filter.filter_motionless_frames(frames_iter)

        slides_iter = self.synchronizer.synchronize(frames_iter, subtitles_iter)

        presentation = self.builder.build(slides_iter)

        presentation_filepath = metadata.filepath.with_suffix(".pptx")
        presentation.save(presentation_filepath)
