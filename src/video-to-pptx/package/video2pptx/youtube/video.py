import typing
from dataclasses import dataclass
from datetime import datetime

from video2pptx.base.video import VideoMetadata


@dataclass
class YouTubeVideoMetadata(VideoMetadata):
    """A class that wraps YouTube video metadata"""
    author: str
    description: str
    keywords: typing.List[str]
    publish_datetime: datetime
    rating: float
    title: str
    views: int
