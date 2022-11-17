import enum
import typing
from dataclasses import dataclass
from datetime import timedelta
from functools import lru_cache


class VideoResolution(str, enum.Enum):
    """An enum class that implements a video resolution hierarchy"""
    lowest  = "lowest"
    random  = "random"
    p144    = "144p"
    p240    = "240p"
    p360    = "360p"
    p480    = "480p"
    p720    = "720p"
    p1080   = "1080p"
    p2160   = "2160p"
    highest = "highest"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    @lru_cache(maxsize=1)
    def hierarchy() -> typing.List["VideoResolution"]:
        return [
            VideoResolution.p144, 
            VideoResolution.p240, 
            VideoResolution.p360, 
            VideoResolution.p480, 
            VideoResolution.p720, 
            VideoResolution.p1080, 
            VideoResolution.p2160
        ]

    @property
    def prev(self) -> typing.Optional["VideoResolution"]:
        hierarchy = VideoResolution.hierarchy()

        try:
            self_idx = hierarchy.index(self)
            return hierarchy[self_idx - 1]
        except ValueError:
            return None
        except IndexError:
            return None

    @property
    def next(self) -> typing.Optional["VideoResolution"]:
        hierarchy = VideoResolution.hierarchy()

        try:
            self_idx = hierarchy.index(self)
            return hierarchy[self_idx + 1]
        except ValueError:
            return None
        except IndexError:
            return None


@dataclass
class BaseVideoMetadata:
    """A base class that wraps video metadata"""
    filepath: str
    caption_filepath: typing.Optional[str]
    duration: timedelta

    def __post_init__(self) -> None:
        if isinstance(self.duration, float):
            self.duration = timedelta(seconds=self.duration)
