import typing
from dataclasses import dataclass
from datetime import datetime

from video2pptx.base.datamodels.video import BaseVideoMetadata


@dataclass
class YouTubeVideoMetadata(BaseVideoMetadata):
    """A class that wraps YouTube video metadata"""

    author: str
    description: str
    keywords: typing.List[str]
    publish_datetime: datetime
    rating: float
    title: str
    views: int
