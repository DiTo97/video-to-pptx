import enum
import typing
from dataclasses import dataclass
from datetime import datetime
from enum import auto


class VideoResolution(enum.Enum):
    """A class that wraps the desired video resolution"""
    lowest  = auto()
    random  = auto()
    highest = auto()


@dataclass
class VideoMetadata:
    author: str
    description: str
    filepath: str
    caption_filepath: typing.Optional[str]
    keywords: typing.List[str]
    publish_datetime: datetime
    rating: float
    title: str
    views: int
