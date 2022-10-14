import enum
import typing
from dataclasses import dataclass
from datetime import datetime
from enum import auto

from video2pttx.video.caption import CaptionType


class VideoResolution(enum.Enum):
    """A class that wraps the desired video resolution"""
    lowest  = auto()
    random  = auto()
    highest = auto()


@dataclass
class VideoMetadata:
    author: str
    caption_str : typing.Optional[str]
    caption_type: typing.Optional[CaptionType]
    description: str
    filepath: str
    keywords: typing.List[str]
    publish_datetime: datetime
    rating: float
    title: str
    views: int
